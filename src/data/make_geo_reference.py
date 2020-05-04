import geopandas as gpd
import os

from pathlib import Path
from src import utils

# get project top directory
base_dir = Path(os.getcwd())
geo_data = base_dir / 'data' / \
           'external' / 'geo_data' / 'ne_50m_admin_0_countries.zip'
geo_reference = base_dir / 'data' / \
                'processed' / 'geo_reference' / 'country_borders.geojson'

country_rename_dict = {
        'country': {
            'Iran (Islamic Republic of)': 'Iran',
            'Libyan Arab Jamahiriya': 'Libya',
            'Syrian Arab Republic': 'Syria',
            'Republic of Moldova': 'Moldova',
            "Côte d'Ivoire": 'Ivory Coast',
            'Viet Nam': 'Vietnam',
            "Lao People's Democratic Republic": 'Laos',
            'Republic of the Congo': 'Congo',
            'Korea, Republic of': 'South Korea',
            'Burma': 'Myanmar',
            'S. Sudan': 'South Sudan',
            'United States of America': 'United States',
            'Congo': 'Congo (Brazzaville)',
            'Dem. Rep. Congo': 'Congo (Kinshasa)',
            'Bosnia and Herz.': 'Bosnia and Herzegovina',
            'Macedonia': 'North Macedonia',
            'Central African Rep.': 'Central African Republic'
        }
    }


def main():
    # load geodataframe
    gdf = gpd.read_file(f'zip://{geo_data}', crs='EPSG:4326')

    # subset dataframe to relevant columns
    COLUMNS = ['NAME', 'geometry']
    gdf_clean = gdf[COLUMNS]
    gdf_clean = gdf_clean.rename(columns={'NAME': 'country'})
    gdf_clean = gdf_clean.replace(country_rename_dict)

    # dir exists check, overwriting in all cases
    utils.check_folder_exists(geo_reference)

    gdf_clean.to_file(geo_reference, driver='GeoJSON')


if __name__ == '__main__':
    main()
