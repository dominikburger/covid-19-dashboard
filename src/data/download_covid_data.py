import os

URL_CSSE_DATA = 'https://github.com/CSSEGISandData/COVID-19'
os.system('rm -rf ./data/external/csse_data/')
os.system(f'git clone {URL_CSSE_DATA} ./data/external/csse_data')