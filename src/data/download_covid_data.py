from src import paths
import shutil
import subprocess


URL_COVID_DATA_GIT: str = 'https://github.com/CSSEGISandData/COVID-19'
URL_COVID_DATA_SVN: str = 'https://github.com/CSSEGISandData/COVID-19' \
                     '/trunk/csse_covid_19_data/csse_covid_19_daily_reports'

DIR_COVID_DOWNLOAD: str = 'csse_covid_19_data/csse_covid_19_daily_reports'


def clean_directory():
    """
    Removes the directory where csse data is stored and creates it afterwards
    """
    shutil.rmtree(paths.dir_csse_data)
    paths.dir_csse_data.mkdir(exist_ok=False)


def do_sparse_checkout():
    """

    """
    result_clone = subprocess.run(
        [
            "git",
            "clone", f"{URL_COVID_DATA_GIT}",
            "--no-checkout", paths.dir_csse_data,
            "--depth", "1"
        ],
        cwd=paths.dir_csse_data,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE
    )
    result_set_sparse = subprocess.run(
        [
            "git", "sparse-checkout",
            "set", f"{DIR_COVID_DOWNLOAD}"
        ],
        cwd=paths.dir_csse_data,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE
    )
    result_checkout = subprocess.run(
        ["git", "checkout", "master"],
        cwd=paths.dir_csse_data,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE
    )


def main():
    clean_directory()
    do_sparse_checkout()


if __name__ == '__main__':
    main()
