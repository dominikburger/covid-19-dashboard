# -*- coding: utf-8 -*-
import click
import logging
import pandas as pd
import geopandas as gpd
import numpy as np

import os
from pathlib import Path

# from dotenv import find_dotenv, load_dotenv

# get project top directory
project_dir = Path(__file__).resolve().parents[2]
csse_data = project_dir / 'data/external/csse_data/csse_covid_19_data'
daily_data = csse_data / 'csse_covid_19_daily_reports/'
ts_data = csse_data / 'csse_covid_19_time_series'
processed_daily_dir = project_dir / 'data' / 'processed' / 'daily_report'


def get_output_path(input_path=None, output_folder=None, suffix='.csv'):
    output_file = f'{Path(input_path).stem}{suffix}'
    output_path = output_folder / output_file
    return output_path


def check_folder(path):
    path = path.parents[0]
    path.mkdir(parents=True, exist_ok=True)


column_schema = {
    'Province/State': 'province',
    'Country/Region': 'country',
    'Last Update': 'last_update',
    'Confirmed': 'confirmed',
    'Deaths': 'deaths',
    'Recovered': 'recovered',
    'Active': 'active',
    'Latitude': 'lat',
    'Longitude': 'long',
    'FIPS': 'fips',
    'Admin2': 'admin2',
    'Province_State': 'province',
    'Country_Region': 'country',
    'Last_Update': 'last_update',
    'Lat': 'lat',
    'Long_': 'long',
    'Combined_Key': 'combined_key'
}

column_list = [
    'confirmed',
    'deaths',
    'recovered',
    'active',
]

index_list = [
    'country',
    'province'
]

aggregation_dict = {
    'confirmed': 'sum',
    'deaths': 'sum',
    'recovered': 'sum',
    'active': 'sum',
    'last_update': 'first'
}

country_rename_dict = {
    'country': {
        ' Azerbaijan': 'Azerbaijan',
        'Hong Kong SAR': 'Hong Kong',
        'Iran (Islamic Republic of)': 'Iran',
        'Bahamas, The': 'Bahamas',
        'US': 'United States',
        'UK': 'United Kingdom',
        'Viet Nam': 'Vietnam',
        'Taipei and environs': 'Taiwan',
        'North Ireland': 'United Kingdom',
        'Macao SAR': 'Macau',
        'Holy See': 'Vatican City',
        'Taiwan*': 'Taiwan',
        "Cote d'Ivoire": 'Ivory Coast',
        'Republic of Ireland': 'Ireland',
        'Republic of Korea': 'South Korea',
        'Republic of Moldova': 'Moldova',
        'Republic of the Congo': 'Congo',
        'Russian Federation': 'Russia',
        'Korea, South': 'South Korea',
        'occupied Palestinian territory': 'Palestine',
        'Cruise Ship': 'Others',
        'Diamond Princess': 'Others',
        'MS Zaandam': 'Others',
        'Reunion': 'France',
        'Channel Islands': 'United Kingdom',
        'Czechia': 'Czech Republic',
        'Mainland China': 'China',
        'Macao': 'Macau',
        'Gambia, The': 'The Gambia',
        'Cape Verde': 'Cabo Verde',
        'Timor-Leste': 'East Timor',
        'St. Martin': 'Saint Martin'
    }
}


def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('preparing daily reports')

    # get all raw daily reports
    path_list = sorted([path for path in daily_data.glob('*.csv')])
    for input_path in path_list:
        # read data
        df = pd.read_csv(input_path)
        # rename columns refering to schema
        df = df.rename(columns=column_schema)
        # replace country names
        df = df.replace(country_rename_dict)
        # add 'active' column if it doesn't exist
        if 'active' not in df.columns:
            df.loc[:, 'active'] = np.nan
        # group by country and province
        df = df.groupby(['country']).agg(aggregation_dict)
        # sort by country and province index)
        df = df.sort_index()
        # change order of columns
        df = df[column_list]

        output_file = get_output_path(
            input_path=input_path,
            output_folder=processed_daily_dir
        )
        # dir exists check, overwriting in all cases
        check_folder(output_file)

        logger.info(f'writing daily report: {output_file}')
        df.to_csv(output_file)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    # load_dotenv(find_dotenv())

    main()
