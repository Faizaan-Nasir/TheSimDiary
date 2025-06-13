import os
import sys
import shutil
import platform

def get_resource_path(relative_path):
    # bundled path being returned
    try:
        base_path = sys._MEIPASS  
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_user_data_path(need):
    # returns AppData for windows and documents for other os
    home = os.path.expanduser("~")

    if platform.system() == "Windows":
        base_dir = os.path.join(os.environ.get("LOCALAPPDATA", os.path.join(home, "AppData", "Local")), "TheSimDiary", "data")
    else:
        base_dir = os.path.join(home, "Documents", "TheSimDiary", "data")

    if need=="log":
        return os.path.join(base_dir, "log.csv")
    elif need=="data":
        return os.path.join(base_dir, "data.csv")
    elif need=="airports":
        return os.path.join(base_dir, "airport-codes.csv")
    else:
        return base_dir

def setup_editable_src(need):
    # should copy bundled data folder to editable data folder
    bundled_src_path = get_resource_path("data")
    user_src_path = get_user_data_path("init")  # Gets base dir: AppData/Documents

    if not os.path.exists(user_src_path):
        print(f"Copying bundled 'data' folder:\nFrom: {bundled_src_path}\nTo:   {user_src_path}")
        shutil.copytree(bundled_src_path, user_src_path)
    if need=="log":
        return os.path.join(user_src_path, "log.csv")
    elif need== "data":
        return os.path.join(user_src_path, "data.csv")
    elif need=="airports":
        return os.path.join(user_src_path, "airport-codes.csv")
