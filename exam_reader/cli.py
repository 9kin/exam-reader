import subprocess
import sys
import time
from pathlib import Path

import click

from .database import Job, db
from .pdf_reader import pdf_workers
from .utils import add_files

dir = Path(__file__).resolve().parent.parent


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo("I was invoked without subcommand")


@cli.command()
@click.option("-c", "--count", default=3, help="Number of workers.")
@click.option("-d", "--debug", default=False, is_flag=True, help="Debug.")
@click.option("-f", "--files", default=0, help="Number of files for debug.")
def worker(count, debug, files):
    if files != 0:
        add_files([dir.joinpath("files", "ege2016.pdf")] * files)
    pdf_workers(workers_count=count, debug=debug, files=files)


@cli.command()
@click.argument("files", nargs=-1, type=click.Path())
def add(files):
    all_files = []
    for file_path in files:
        full_file_path = dir.joinpath(file_path)
        if not full_file_path.is_file() or not full_file_path.exists():
            continue
        all_files.append(full_file_path)
    add_files(all_files)


PROMPT = "❯"


def slowprint(s):
    for c in s + "\n":
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.05)


def show(command, execute=True):
    print(PROMPT, end=" ")
    slowprint(command)
    if execute:
        start = time.time()
        subprocess.call("python3 -m " + command, shell=True)
        print(f"took {int(time.time()  - start)}s", end="")


@cli.command()
def debug_worker_speed():
    db.drop_tables([Job])
    db.create_tables([Job])
    show("exam_reader worker -c 2 -d -f 2")


@cli.command()
def debug_worker():
    db.drop_tables([Job])
    db.create_tables([Job])
    show("exam_reader worker -c 2 -d")


"""
termtosvg docs/source/static/debug_worker_speed.svg --command='python3 -m exam_reader debug-worker-speed' --screen-geometry=80x3


"""
