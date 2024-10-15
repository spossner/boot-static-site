from folder import *

from pathlib import Path

ROOT_DIR = Path(__file__).parents[1]

def main():
    clean(ROOT_DIR.joinpath("public"))

if __name__ == "__main__":
    main()
