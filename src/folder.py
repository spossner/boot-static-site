import os
import shutil


def clean(path):
    if not path.exists():
        path.mkdir()
        return

    for p in path.iterdir():
        if p.is_file():
            p.unlink()
        elif p.is_dir():
            clean(p)
            p.rmdir()


def copy(src, dest):
    for p in src.iterdir():
        if p.is_file():
            shutil.copy(p, dest)
        elif p.is_dir():
            q = dest / p.name
            q.mkdir()
            copy(p, q)
