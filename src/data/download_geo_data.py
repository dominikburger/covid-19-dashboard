import os
from src import paths

URL_GEO_DATA = 'https://www.naturalearthdata.com/\
http//www.naturalearthdata.com/download/110m/' \
'cultural/ne_110m_admin_0_countries.zip'

os.system(f'curl {URL_GEO_DATA} -L -o {paths.file_geo_data} --create-dirs')
