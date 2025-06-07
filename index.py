import sys
from PyQt5.QtWidgets import *
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5.QtGui import *
import os
from components.stats import Stats
from utils import resource_path

base_dir = resource_path()


if __name__=="__main__":
    app = QApplication([])
    window = Stats()
    window.show()
    appexe=app.exec()
    sys.exit(appexe)