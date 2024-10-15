import os


def clean(path):
    if not path.exists():
        path.mkdir()
        return
    for p in path.iterdir():
        if p.is_dir():
            clean(p)
            p.rmdir()
        else:
            p.unlink()