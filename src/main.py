from folder import *

from pathlib import Path

ROOT_DIR = Path(__file__).parents[1]

def main():
    public = ROOT_DIR.joinpath("public")
    static = ROOT_DIR.joinpath("static")
    clean(public)
    copy(static, public)

if __name__ == "__main__":
    main()
