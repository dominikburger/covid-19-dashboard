import os
from src import paths


def main():
    os.system(
        f'cd {paths.dir_csse_data} && '
        f'git reset --hard origin/master && '
        f'git pull origin master'
    )


if __name__ == '__main__':
    main()
