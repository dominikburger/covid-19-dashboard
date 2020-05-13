import os
import argparse

URL_COVID_DATA_GIT = 'https://github.com/CSSEGISandData/COVID-19'
URL_COVID_DATA_SVN = 'https://github.com/CSSEGISandData/COVID-19' \
                     '/trunk/csse_covid_19_data/csse_covid_19_daily_reports'
OUTPUT_FOLDER = 'data/external/csse_data/' \
                'csse_covid_19_data/csse_covid_19_daily_reports/'


def main(vcs):
    if vcs == 'git':
        os.system('rm -rf ./data/external/covid_data/')
        os.system(f'git clone {URL_COVID_DATA_GIT} {OUTPUT_FOLDER}')
    elif vcs == 'svn':
        os.system(f'svn export --force {URL_COVID_DATA_SVN} {OUTPUT_FOLDER}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'vcs',
        default='git',
        type=str,
        help='Specifies the utilized version control system'
    )
    args = parser.parse_args()

    main(vcs=args.vcs)
