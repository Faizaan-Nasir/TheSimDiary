import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import QtGui
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
matplotlib.use('Qt5Agg')
from PyQt5.QtGui import *
import os
import urllib

base_dir = os.path.dirname(__file__)

class Guide(QWidget):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.setWindowTitle("Pilot Diary")
        self.setFixedWidth(1400)
        self.setFixedHeight(760)
        pixmap = QPixmap(os.path.join(base_dir, 'src', 'background.jpg'))
        palette = self.palette()
        palette.setBrush(QPalette.Background, QBrush(pixmap))
        self.setPalette(palette)
        self.setWindowIcon(QtGui.QIcon('./src/icon.ico'))

        self.showUI()
    
    def funGoBack(self):
        self.deleteLater()

    def showUI(self):
        self.subheadingStyle='''background: transparent;font-size:25px;font-weight:600;border-radius:10px;color:#515151'''
        self.heading=QLabel('Useful Tools',parent=self)
        self.heading.setFixedWidth(1350)
        self.heading.move(0,40)
        self.heading.setAlignment(QtCore.Qt.AlignCenter)
        self.heading.setStyleSheet("background:rgba(255, 255, 255, 0.725);font-size:45px;font-weight:800;padding:8px;margin-left:50px;border-radius:10px;color:#515151")

        self.goBack=QPushButton("< Go Back",parent=self)
        self.goBack.move(80,57)
        self.goBack.setStyleSheet("background:transparent;font-size:18px;font-weight:800;color:#515151")
        self.goBack.clicked.connect(self.funGoBack)

        self.background1=QWidget(self)
        self.background1.setFixedSize(423,595)
        self.background1.setStyleSheet("QWidget { background: rgba(255, 255, 255, 0.725); border-radius: 10px; }")
        self.background1.move(50,125)

        self.subheading1=QLabel("Planning & Dispatch",parent=self.background1)
        self.subheading1.setStyleSheet(self.subheadingStyle)
        self.subheading1.setFixedWidth(423)
        self.subheading1.setAlignment(QtCore.Qt.AlignCenter)
        self.subheading1.move(0,30)

        self.label1 = QLabel('<a href="https://www.simbrief.com/" style="color: #515151">SimBrief - Flight Planner</a>',parent=self.background1)
        self.label1.setOpenExternalLinks(True)
        self.label1.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.label1.setFixedWidth(423)
        self.label1.move(0,80)
        self.label1.setAlignment(QtCore.Qt.AlignCenter)
        self.label1.setStyleSheet("font-size: 20px; background: transparent;")

        self.background2=QWidget(self)
        self.background2.setFixedSize(424,595)
        self.background2.setStyleSheet("QWidget { background: rgba(255, 255, 255, 0.725); border-radius: 10px; }")
        self.background2.move(488,125)

        self.subheading2=QLabel("Networks & Maps",parent=self.background2)
        self.subheading2.setStyleSheet(self.subheadingStyle)
        self.subheading2.setFixedWidth(424)
        self.subheading2.setAlignment(QtCore.Qt.AlignCenter)
        self.subheading2.move(0,30)

        self.background3=QWidget(self)
        self.background3.setFixedSize(423,595)
        self.background3.setStyleSheet("QWidget { background: rgba(255, 255, 255, 0.725); border-radius: 10px; }")
        self.background3.move(927,125)

        self.subheading3=QLabel("Miscellaneous",parent=self.background3)
        self.subheading3.setStyleSheet(self.subheadingStyle)
        self.subheading3.setFixedWidth(423)
        self.subheading3.setAlignment(QtCore.Qt.AlignCenter)
        self.subheading3.move(0,30)

if __name__=="__main__":
    app = QApplication([])
    window = Guide()
    window.show()
    appexe=app.exec()
    sys.exit(appexe)



        
