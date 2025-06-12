import os
import sys
import shutil
import platform

def get_resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and PyInstaller.
    """
    try:
        # PyInstaller temporary folder
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_user_data_path(need):
    """
    Returns a writable user path inside Documents/TheSimDiary/data
    Works cross-platform: Windows, macOS, Linux
    """
    home = os.path.expanduser("~")

    if platform.system() == "Windows":
        documents = os.path.join(os.environ.get("USERPROFILE", home), "Documents")
    else:
        documents = os.path.join(home, "Documents")
    if need=="log":
        return os.path.join(documents, "TheSimDiary", "data","log.csv")
    elif need=="data":
        return os.path.join(documents, "TheSimDiary", "data","data.csv")
    elif need=="airports":
        return os.path.join(documents, "TheSimDiary", "data","airport-codes.csv")
    else:
        return os.path.join(documents, "TheSimDiary", "data")

def setup_editable_src(need):
    """
    Copy bundled data folder to user writable folder if missing.
    Returns the path to the editable src folder.
    """
    bundled_src_path = get_resource_path("data")
    user_src_path = get_user_data_path("init")

    if not os.path.exists(user_src_path):
        print(f"Copying bundled 'data' folder:\nFrom: {bundled_src_path}\nTo:   {user_src_path}")
        shutil.copytree(bundled_src_path, user_src_path)
    if need=="log":
        return os.path.join(user_src_path,"log.csv")
    elif need=="data":
        return os.path.join(user_src_path,"data.csv")
    elif need=="airports":
        return os.path.join(user_src_path,"airport-codes.csv")

