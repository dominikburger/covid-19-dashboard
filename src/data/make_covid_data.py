import os

URL_CSSE_DATA = 'https://github.com/CSSEGISandData/COVID-19'
os.system(f'rm -rf ./data/external/csse_data/ && git clone {URL_CSSE_DATA} ./data/external/csse_data')
