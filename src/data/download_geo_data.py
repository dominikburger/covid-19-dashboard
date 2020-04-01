import os

URL_GEO_DATA = 'https://www.naturalearthdata.com/\
http//www.naturalearthdata.com/download/50m/cultural/ne_50m_admin_0_countries.zip'

os.system(f'curl {URL_GEO_DATA} -L -o ./data/external/geo_data/ne_50m_admin_0_countries.zip --create-dirs ')
