from multiprocessing import JoinableQueue, Pool, Process
import camelot
import fitz  # mupdf
import pandas as pd
from PIL import Image, ImageDraw

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


def extract_pdf(filepath):
    tables = camelot.read_pdf(
        filepath,
        pages="all",
        split_text=True,
    )
    # https://stackoverflow.com/questions/58837504/camelot-pdf-extraction-fail-parsing
    print(pd.concat([table.df for table in tables]).to_string())

    img_array, table_bbox = tables[0]._image

    doc = fitz.open(filepath)
    page = doc[0]
    blocks = blocks_without_table(
        page.getTextPage().extractBLOCKS(), table_bbox
    )  # faster than page.getText("blocks")

    for block in blocks:
        print(block[4])

    img = Image.fromarray(img_array, "RGB")
    draw = ImageDraw.Draw(img)

    for block in blocks + list(table_bbox):
        draw.rectangle(
            (block[0], block[1], block[2], block[3]),
            outline=(255, 0, 0),
            width=3,
        )
    img.save("tmp.png")

def process_job(q):
    while True:
        next_job = q.get()
        next_job[0](*next_job[1:])
        q.task_done()



def main(dir):
    pdf_documents = [str(dir.joinpath("ege2016rus.pdf"))] * 5
    #with Pool(3) as p:
    #    print(p.map(extract_pdf, pdf_documents))
    queue = JoinableQueue()
    for document in pdf_documents:
        queue.put((extract_pdf, document))
    workers = [Process(target=process_job, args=(queue,)),
               Process(target=process_job, args=(queue,)),
               Process(target=process_job, args=(queue,))]
    for worker in workers:
        worker.daemon = True
        worker.start()
    queue.join()
