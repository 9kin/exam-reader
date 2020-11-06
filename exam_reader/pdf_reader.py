from multiprocessing import JoinableQueue, Process, Queue, Value

import camelot
import fitz
import pandas as pd
from PIL import Image, ImageDraw

from .bar_utils import ProcessBar
from .database import Job, db
from .utils import simple_job

ZOOM_FACTOR = 4.166106501051772


def blocks_without_table(blocks, table_bbox):
    blocks = [
        (
            block[0] * ZOOM_FACTOR,
            block[1] * ZOOM_FACTOR,
            block[2] * ZOOM_FACTOR,
            block[3] * ZOOM_FACTOR,
            block[4],
            block[5],
            block[6],
        )
        for block in blocks
    ]
    rects = [
        fitz.Rect(table_pos[0], table_pos[1], table_pos[2], table_pos[3])
        for table_pos in table_bbox.keys()
    ]
    blocks = [
        block
        for block in blocks
        if all(map(lambda rect: fitz.Rect(block[:4]) not in rect, rects))
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
    def __init__(self, workers_cnt, queue, db_queue, debug):
        self.workers = []
        self.pending = Value("i", 0)
        self.cnt = Value("i", 0)

        for _ in range(workers_cnt):
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

    additional = Job.select().where(Job.status == 1).count()

    Job.update(status=0).where(Job.status == 1).execute()

    progress_bar = ProcessBar(additional + files, debug=files != 0)

    queue = JoinableQueue()
    db_queue = Queue()
    workers = Workers(workers_count, queue, db_queue, files == 0)

    while True:
        if files != 0 and Job.select().where(Job.status != 2).count() == 0:
            break

        progress_bar.update((workers.cnt.value - progress_bar.value))
        if not db_queue.empty():
            jobs = []
            while not db_queue.empty():
                jobs.append(db_queue.get())
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
