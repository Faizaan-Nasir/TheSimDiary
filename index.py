import sys
from PyQt5.QtWidgets import *
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5.QtGui import *
import os
from components.stats import Stats

base_dir = os.path.dirname(__file__)


if __name__=="__main__":
    app = QApplication([])
    window = Stats()
    window.show()
    appexe=app.exec()
    sys.exit(appexe)