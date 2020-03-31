import os
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
dir_csse = project_root / './data/external/csse_data'

os.chdir(dir_csse)
os.system('git fetch && git pull')
