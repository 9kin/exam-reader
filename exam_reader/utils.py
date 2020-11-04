from random import randint
from time import sleep

from .database import Job, db


def add_files(files):

    if db.is_closed():
        db.connect()

    db.create_tables([Job])

    pdf_documents = []
    for file in files:
        pdf_documents.append(Job(path=file, status=0))

    with db.atomic():
        Job.bulk_create(pdf_documents, batch_size=100)


def simple_job():
    sleep(randint(1, 3) / 10)
