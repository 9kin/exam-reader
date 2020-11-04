from multiprocessing import JoinableQueue, Process, Queue, Value

import camelot
import fitz
import pandas as pd
from PIL import Image, ImageDraw

from .bar_utils import Bar
from .database import Job, db
from .utils import simple_job

C = 4.166106501051772


def blocks_without_table(blocks, table_bbox):
    blocks = [
        (b[0] * C, b[1] * C, b[2] * C, b[3] * C, b[4], b[5], b[6])
        for b in blocks
    ]
    rects = [
        fitz.Rect(table_pos[0], table_pos[1], table_pos[2], table_pos[3])
        for table_pos in table_bbox.keys()
    ]
    blocks = [
        b
        for b in blocks
        if all(map(lambda x: fitz.Rect(b[:4]) not in x, rects))
    ]
    return blocks


def extract_pdf(job, debug):
    if debug:
        print(job.id, "start")

    tables = camelot.read_pdf(
        job.path,
        pages="all",
        split_text=True,
    )
    # https://stackoverflow.com/questions/58837504/camelot-pdf-extraction-fail-parsing
    # print(pd.concat([table.df for table in tables]).to_string())

    img_array, table_bbox = tables[0]._image

    doc = fitz.open(job.path)
    page = doc[0]
    blocks = blocks_without_table(
        page.getTextPage().extractBLOCKS(), table_bbox
    )  # faster than page.getText("blocks")

    # for block in blocks:
    #    print(block[4])

    img = Image.fromarray(img_array, "RGB")
    draw = ImageDraw.Draw(img)

    for block in blocks + list(table_bbox):
        draw.rectangle(
            (block[0], block[1], block[2], block[3]),
            outline=(255, 0, 0),
            width=3,
        )

    if debug:
        print(job.id, "end")


def process_job(workers, queue, db_queue, debug):
    while True:
        job = queue.get()

        workers.do()
        extract_pdf(job, debug)
        workers.end()

        job.status = 2
        db_queue.put(job)
        queue.task_done()


class Workers:
    def __init__(self, workers_cnt, queue, db_queue, debug, bar):
        self.workers = []
        self.pending = Value("i", 0)
        self.cnt = Value("i", 0)
        self.bar = bar

        for i in range(workers_cnt):
            worker = Process(
                target=process_job, args=(self, queue, db_queue, debug)
            )
            worker.daemon = True
            worker.start()
            self.workers.append(worker)

    def do(self):
        self.pending.value += 1

    def end(self):
        self.cnt.value += 1
        self.pending.value -= 1

    def __len__(self):
        return len(self.workers)


def pdf_workers(workers_count=2, debug=True, files=0):
    if db.is_closed():
        db.connect()

    bar = Bar(files, debug=files != 0)

    queue = JoinableQueue()
    db_queue = Queue()
    workers = Workers(workers_count, queue, db_queue, files == 0, bar)

    Job.update(status=0).where(Job.status == 1).execute()

    if files != 0:
        condition = lambda: Job.select().where(Job.status != 2).count() > 0
    else:
        condition = lambda: True

    while condition():
        bar.update((workers.cnt.value - bar.val))
        if not db_queue.empty():
            jobs = []
            while not db_queue.empty():
                q = db_queue.get()
                jobs.append(q)
            with db.atomic():
                Job.bulk_update(jobs, fields=["status"], batch_size=100)
        elif workers_count - queue.qsize() > 0:
            additional_jobs = min(
                Job.select().where(Job.status == 0).count(),
                len(workers) - workers.pending.value,
            )
            if additional_jobs == 0:
                continue
            jobs = []
            for job in (
                Job.select()
                .where(Job.status == 0)
                .paginate(1, additional_jobs)
            ):
                job.status = 1
                jobs.append(job)
            with db.atomic():
                Job.bulk_update(jobs, fields=["status"], batch_size=100)
            for job in jobs:
                queue.put(job)

    queue.join()
    db.close()
