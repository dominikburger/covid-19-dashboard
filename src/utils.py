import src.paths as paths
from datetime import datetime as dt
import os
import json
import pandas as pd


def check_folder_exists(path):
    path = path.parents[0]
    path.mkdir(parents=True, exist_ok=True)


def get_day_range():
    files = paths.dir_processed_daily.glob('*.csv')
    dates = [dt.strptime(filename.stem, '%m-%d-%Y') for filename in files]

    return min(dates), max(dates)


def make_dataframe(path=None, days=None):
    dataframe = pd.DataFrame()

    for day in days:
        temp = pd.read_csv(path / f'{day}.csv')
        temp.loc[:, 'date'] = pd.to_datetime(day)
        dataframe = dataframe.append(temp)

    return dataframe

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
    paths.dir_csse_data.mkdir(parents=True, exist_ok=True)
    paths.dir_processed_daily.mkdir(parents=True, exist_ok=True)
    external_empty = not(any(paths.dir_csse_data.iterdir()))

    if not external_empty:
        print("updating covid data...")
        os.system('python3 src/data/update_covid_data.py')
        print("preparing cleaned dataset...")
        os.system('python3 src/data/make_dataset.py')
    else:
        print("covid data does not exist, downloading...")
        os.system('python3 src/data/download_covid_data.py')
        print("preparing cleaned dataset...")
        os.system('python3 src/data/make_dataset.py')
