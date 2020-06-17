from src import paths
from datetime import datetime as dt
import os
import json
import pandas as pd
from src.data import download_covid_data
from src.data import update_covid_data
from src.data import download_geo_data
from src.data import make_geo_reference
from src.data import make_dataset

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
    print(str(paths.file_geo_reference))
    print(paths.file_geo_reference.is_file())
    if paths.file_geo_reference.is_file():
        print("geo reference exists")
    else:
        print("geo reference does not exist, downloading...")
        download_geo_data.main()
        print("Creating geo reference...")
        make_geo_reference.main()


def load_geo_reference():
    return json.load(open(str(paths.file_geo_reference)))


def parse_covid_data():
    paths.dir_csse_data.mkdir(parents=True, exist_ok=True)
    paths.dir_processed_daily.mkdir(parents=True, exist_ok=True)
    external_empty = not(any(paths.dir_csse_data.iterdir()))

    if not external_empty:
        print("updating covid data...")
        update_covid_data.main()
        print("preparing cleaned dataset...")
        make_dataset.main()
    else:
        print("covid data does not exist, downloading...")
        download_covid_data.main()
        print("preparing cleaned dataset...")
        make_dataset.main()
