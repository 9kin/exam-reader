from os import system
from pathlib import Path


def lint():
    import isort

    app_dir = Path(__file__).resolve().parent.parent
    doc_dir = Path(__file__).resolve().parent.joinpath("docs")
    source_dir = app_dir.joinpath("exam_reader")

    files = (
        list(app_dir.glob("*.py"))
        + list(doc_dir.rglob("*.py"))
        + list(source_dir.glob("*.py"))
    )

    for file in files:
        isort.file(file)
        system(f"black {file} --line-length 79")
