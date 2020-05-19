import geopandas as gpd
import os
from src import utils
from src import paths


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
            'Central African Rep.': 'Central African Republic',
            'W. Sahara': 'Western Sahara',
            'Dominican Rep.': 'Dominican Republic',
            'Eq. Guinea': 'Equatorial Guinea',
            'eSwatini': 'Eswatini',
            'Timor-Leste': 'East Timor'
        }
    }


def main():
    # load geodataframe
    gdf = gpd.read_file(f'zip://{paths.file_geo_data}', crs='EPSG:4326')

    # subset dataframe to relevant columns
    COLUMNS = ['NAME', 'geometry']
    gdf_clean = gdf[COLUMNS]
    gdf_clean = gdf_clean.rename(columns={'NAME': 'country'})
    gdf_clean = gdf_clean.replace(country_rename_dict)

    # dir exists check, overwriting in all cases
    utils.check_folder_exists(paths.file_geo_reference)
    gdf_clean.to_file(paths.file_geo_reference, driver='GeoJSON')


if __name__ == '__main__':
    main()
