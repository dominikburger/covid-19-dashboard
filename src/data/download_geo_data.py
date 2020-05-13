import os

URL_GEO_DATA = 'https://www.naturalearthdata.com/\
http//www.naturalearthdata.com/download/110m/cultural/ne_110m_admin_0_countries.zip'

os.system(f'curl {URL_GEO_DATA} -L -o ./data/external/geo_data/ne_110m_admin_0_countries.zip --create-dirs ')
