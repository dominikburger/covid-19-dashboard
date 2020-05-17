import os
import argparse
from src import paths

URL_COVID_DATA_GIT = 'https://github.com/CSSEGISandData/COVID-19'
URL_COVID_DATA_SVN = 'https://github.com/CSSEGISandData/COVID-19' \
                     '/trunk/csse_covid_19_data/csse_covid_19_daily_reports'

DIR_COVID_DOWNLOAD = 'csse_covid_19_data/csse_covid_19_daily_reports'


def main():
    os.system(
        f'rm -r {paths.dir_csse_data} && mkdir {paths.dir_csse_data} &&'
        f'cd {paths.dir_csse_data} &&'
        f'git init &&'
        f'git remote add -f origin {URL_COVID_DATA_GIT} &&'
        f'git config core.sparseCheckout true &&'
        f'echo "{DIR_COVID_DOWNLOAD}" >> .git/info/sparse-checkout &&'
        f'git pull origin master'
    )


if __name__ == '__main__':
    main()
