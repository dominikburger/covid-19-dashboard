from src import paths
from datetime import datetime as dt
import json
import pandas as pd
from src.data import download_covid_data
from src.data import update_covid_data
from src.data import download_geo_data
from src.data import make_geo_reference
from src.data import make_dataset


def check_folder_exists(path):
    """
    This function checks if a directory exists. If not, the directory will be
    created instead.
    :param path: path of a given directory
    :type path: object of class Pathlib
    :return: None
    :rtype: None
    """
    path = path.parents[0]
    path.mkdir(parents=True, exist_ok=True)


def get_day_range():
    """
    Checks the content of the directory containing the processed csv files and
    returns the minimum and maximum date.
    :return: tuple containing min and max date.
    :rtype: datetime
    """
    files = paths.dir_processed_daily.glob('*.csv')
    dates = [dt.strptime(filename.stem, '%m-%d-%Y') for filename in files]

    return min(dates), max(dates)


def make_dataframe(path=None, days=None):
    """
    Creates a dataframe from a list of csv files by appending them.
    :param path: path of a given directory
    :type path: object of class pathlib.Path
    :param days: string representation of file names of the processed daily
        case files.
    :type days: list
    :return: dataframe
    :rtype: pandas.DataFrame
    """
    dataframe = pd.DataFrame()

    for day in days:
        temp = pd.read_csv(path / f'{day}.csv')
        temp.loc[:, 'date'] = pd.to_datetime(day)
        dataframe = dataframe.append(temp)

    return dataframe


def parse_geo_reference():
    """
    Checks for the existence of the geo reference file which is used for
    the country boarders in the dashboard map graph. If it does not exist,
    the file is downloaded and parsed to a geojson.
    :return: None
    :rtype: None
    """
    if paths.file_geo_reference.is_file():
        print("geo reference exists")
    else:
        print("geo reference does not exist, downloading...")
        download_geo_data.main()
        print("Creating geo reference...")
        make_geo_reference.main()


def load_geo_reference():
    """
    Loads the parsed geo reference file from disk.
    :return: a dictionary containing the geo reference (country boarders) in
        geojson format.
    :rtype: dict
    """
    return json.load(open(str(paths.file_geo_reference)))


def parse_covid_data():
    """
    Downloads the covid-19 data from the csse repository, prepares the files and
    parses them to create the final dataset. Checks if the corresponding
    directories exist, and creates them in case they are non-existent.
    :return: None
    :rtype: None
    """
    paths.dir_csse_data.mkdir(parents=True, exist_ok=True)
    paths.dir_processed_daily.mkdir(parents=True, exist_ok=True)
    external_empty = not (any(paths.dir_csse_data.iterdir()))

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
