import os
from src import paths


def main():
    os.chdir(f'{paths.dir_csse_data}')
    os.system('git fetch && git pull')


if __name__ == '__main__':
    main()

