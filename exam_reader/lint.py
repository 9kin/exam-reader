from os import system
from pathlib import Path

def lint():
    import isort
    APP_DIR = Path(__file__).resolve().parent.parent
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
