# utils.py
import sys
import os

def resource_path(relative_path=""):
    """ Get absolute path to resource for both development and PyInstaller """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
