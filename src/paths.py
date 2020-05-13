from pathlib import Path

dir_project = Path().cwd()
dir_data_external = dir_project / 'data' / 'external'
dir_csse_data = dir_data_external / 'csse_data'
dir_covid_data = dir_csse_data / 'csse_covid_19_data'
dir_daily_data = dir_covid_data / 'csse_covid_19_daily_reports'
dir_ts_data = dir_covid_data / 'csse_covid_19_time_series'
dir_geo_data = dir_data_external / 'geo_data'
dir_processed = dir_project / 'data' / 'processed'
dir_processed_daily = dir_processed / 'daily_report'
dir_processed_geo_reference = dir_processed / 'geo_reference'
dir_assets = dir_project / 'src' / 'visualization' / 'assets'


file_geo_data = dir_geo_data / 'ne_110m_admin_0_countries.zip'
file_geo_reference = dir_processed_geo_reference / 'country_borders.geojson'
