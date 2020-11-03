from multiprocessing import JoinableQueue, Process, Queue
from pathlib import Path

import camelot
import fitz  # mupdf
import pandas as pd
from PIL import Image, ImageDraw

from .database import PQueue, db

C = 4.166106501051772


def insert_test_files():
    if db.is_closed():
        db.connect()
    dir = Path(__file__).resolve().parent.parent.joinpath("files")
    db.drop_tables([PQueue])
    db.create_tables([PQueue])

    pdf_documents = []
    for i in range(15):
        pdf_documents.append(
            PQueue(path=dir.joinpath("ege2016rus.pdf"), status=0)
        )

    with db.atomic():
        PQueue.bulk_create(pdf_documents, batch_size=100)


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


def extract_pdf(filepath):
    tables = camelot.read_pdf(
        filepath,
        pages="all",
        split_text=True,
    )
    # https://stackoverflow.com/questions/58837504/camelot-pdf-extraction-fail-parsing
    # print(pd.concat([table.df for table in tables]).to_string())

    img_array, table_bbox = tables[0]._image

    doc = fitz.open(filepath)
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
    # img.save("tmp.png")
    print(filepath, "extracttion finished")


def process_job(queue, db_queue):
    while True:
        job = queue.get()

        extract_pdf(job.path)
        job.status = 2

        db_queue.put(job)
        queue.task_done()


def database_worker(workers_cnt, queue, db_queue):
    while True:
        if not db_queue.empty():
            jobs = []
            while not db_queue.empty():
                q = db_queue.get()
                jobs.append(q)
            with db.atomic():
                PQueue.bulk_update(jobs, fields=["status"], batch_size=100)
        if PQueue.select().where(PQueue.status == 0).count() > 0:
            jobs = []
            for job in (
                PQueue.select()
                .where(PQueue.status == 0)
                .paginate(1, workers_cnt)
            ):
                job.status = 1
                jobs.append(job)
            with db.atomic():
                PQueue.bulk_update(jobs, fields=["status"], batch_size=100)
            for job in jobs:
                queue.put(job)


def workers(workers_cnt=3):
    if db.is_closed():
        db.connect()
    queue = JoinableQueue()
    db_queue = Queue()

    workers = []
    for i in range(workers_cnt):
        worker = Process(target=process_job, args=(queue, db_queue))
        worker.daemon = True
        worker.start()
        workers.append(worker)

    db_worker = Process(
        target=database_worker, args=(workers_cnt, queue, db_queue)
    )
    db_worker.daemon = True
    db_worker.start()

    import time

    time.sleep(2)

    queue.join()
    db.close()
