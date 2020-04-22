import os
from pathlib import Path


def main():
    project_dir = Path(__file__).resolve().parents[2]
    dir_csse = project_dir / './data/external/csse_data'

    os.chdir(dir_csse)
    os.system('git fetch && git pull')


if __name__ == '__main__':
    main()

