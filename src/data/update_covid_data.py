import os
from src import paths
import subprocess


def main():
    result_gc = subprocess.run(
        ["git", "gc"],
        cwd=paths.dir_csse_data,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE
    )
    result_reset = subprocess.run(
        ["git", "reset", "--hard", "origin/master"],
        cwd=paths.dir_csse_data,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE
    )
    result_pull = subprocess.run(
        ["git", "pull", "origin", "master"],
        cwd=paths.dir_csse_data,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE
    )


if __name__ == '__main__':
    main()
