def check_folder_exists(path):
    path = path.parents[0]
    path.mkdir(parents=True, exist_ok=True)
