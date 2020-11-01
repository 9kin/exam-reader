from os import system
from pathlib import Path

import isort


def main():
    APP_DIR = Path(__file__).resolve().parent
    DOCS_DIR = Path(__file__).resolve().parent.joinpath("docs")
    PY_APP_DIR = APP_DIR.joinpath("exam_reader")

    files = (
        list(APP_DIR.glob("*.py"))
        + list(DOCS_DIR.rglob("*.py"))
        + list(PY_APP_DIR.glob("*.py"))
    )

    for file in files:
        isort.file(file)
        system(f"black {file} --line-length 79")


if __name__ == "__main__":
    main()
