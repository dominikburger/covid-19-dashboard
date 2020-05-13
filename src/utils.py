import src.paths as paths
from datetime import datetime as dt
import os
import json


def check_folder_exists(path):
    path = path.parents[0]
    path.mkdir(parents=True, exist_ok=True)


def get_day_range():
    files = paths.dir_processed_daily.glob('*.csv')
    dates = [dt.strptime(filename.stem, '%m-%d-%Y') for filename in files]

    return min(dates), max(dates)


def parse_geo_reference():
    if paths.file_geo_reference.is_file():
        print("geo reference exists")
    else:
        print("geo reference does not exist, downloading...")
        os.system('python3 src/data/download_geo_data.py')
        print("Creating geo reference...")
        os.system('python3 src/data/make_geo_reference.py')


def load_geo_reference():
    return json.load(open(str(paths.file_geo_reference)))


def parse_covid_data():
    paths.dir_processed_daily.mkdir(parents=True, exist_ok=True)

    is_empty = not(any(paths.dir_processed_daily.iterdir()))
    if is_empty:
        print("covid data does not exist, downloading...")
        os.system('python3 src/data/download_covid_data.py')
        print("preparing cleaned dataset...")
        os.system('python3 src/data/make_dataset.py')
    else:
        print("updating covid data...")
        os.system('python3 src/data/update_covid_data.py')
        print("preparing cleaned dataset...")
        os.system('python3 src/data/make_dataset.py')
