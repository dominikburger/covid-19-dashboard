import os
from src import paths
import subprocess


URL_GEO_DATA = 'https://www.naturalearthdata.com/\
http//www.naturalearthdata.com/download/110m/' \
'cultural/ne_110m_admin_0_countries.zip'


def main():
    result_download = subprocess.run(
        [
            "curl", URL_GEO_DATA, "-L", "-o",
            paths.file_geo_data,
            "--create-dirs",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE
    )


if __name__ == '__main__':
    main()
