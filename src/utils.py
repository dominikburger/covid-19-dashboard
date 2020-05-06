import src.paths as paths
from datetime import datetime as dt


def check_folder_exists(path):
    path = path.parents[0]
    path.mkdir(parents=True, exist_ok=True)


def get_day_range():
    files = paths.dir_processed.glob('*.csv')
    dates = [dt.strptime(filename.stem, '%m-%d-%Y') for filename in files]

    return min(dates), max(dates)
