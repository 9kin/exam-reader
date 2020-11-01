import datetime
from pathlib import Path

from exam_reader.pdf_reader import main

if __name__ == "__main__":
    start = datetime.datetime.now()
    main(dir=Path(__file__).resolve().parent.joinpath("files"))
    end = datetime.datetime.now()
    print(end - start)
