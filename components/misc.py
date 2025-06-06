import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import QtGui
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
matplotlib.use('Qt5Agg')
from PyQt5.QtGui import *
import os

base_dir = os.path.dirname(os.path.dirname(__file__))
class Misc(QWidget):
    def __init__(self,parent,**kwargs):
        super().__init__(**kwargs)
        self.setWindowTitle("Pilot Diary")
        self.setFixedWidth(1400)
        self.setFixedHeight(760)
        self.parent=parent
        pixmap = QPixmap(os.path.join(base_dir, 'src', 'background.jpg'))
        palette = self.palette()
        palette.setBrush(QPalette.Background, QBrush(pixmap))
        self.setPalette(palette)
        self.setWindowIcon(QtGui.QIcon('./src/icon.ico'))

        self.showUI()
    
    def funGoBack(self):
        self.parent.show()
        self.deleteLater()

    def showUI(self):
        self.subheadingStyle='''background: transparent;font-size:25px;font-weight:600;color:#515151'''
        self.heading=QLabel('Miscellaneous',parent=self)
        self.heading.setFixedWidth(1350)
        self.heading.move(0,40)
        self.heading.setAlignment(QtCore.Qt.AlignCenter)
        self.heading.setStyleSheet("background:rgba(255, 255, 255, 0.725);font-size:45px;font-weight:800;padding:8px;margin-left:50px;border-radius:10px;color:#515151")

        self.goBack=QPushButton("< Go Back",parent=self)
        self.goBack.move(80,57)
        self.goBack.setStyleSheet("background:transparent;font-size:18px;font-weight:800;color:#515151")
        self.goBack.clicked.connect(self.funGoBack)

        self.background1=QWidget(self)
        self.background1.setFixedSize(700,595)
        self.background1.setStyleSheet("QWidget { background: rgba(255, 255, 255, 0.725); border-radius: 10px; }")
        self.background1.move(50,125)

        self.subheading1=QLabel("Useful Tools",parent=self.background1)
        self.subheading1.setStyleSheet(self.subheadingStyle)
        self.subheading1.setFixedWidth(700)
        self.subheading1.setAlignment(QtCore.Qt.AlignCenter)
        self.subheading1.move(0,30)

        subSubHeadingsStyle='background: transparent;font-size:22px;font-weight:600;color:#515151'
        linksStyle='''QLabel{
            background: transparent;
            font-size:20px;
            font-weight:400;
            color:#515151;
        }
        QLabel:hover{
            color:#515151;
        }'''

        self.planHeading = QLabel("Planning & Dispatch:", parent=self.background1)
        self.planHeading.setStyleSheet(subSubHeadingsStyle)
        self.planHeading.move(80, 90)

        self.simBrief = QLabel('•&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="https://www.simbrief.com/">SimBrief</a> - Flight Planner', parent=self.background1)
        self.simBrief.setOpenExternalLinks(True)
        self.simBrief.setTextFormat(QtCore.Qt.RichText)
        self.simBrief.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.simBrief.setStyleSheet(linksStyle)
        self.simBrief.move(80, 130)

        self.navigraph = QLabel('•&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="https://www.navigraph.com/">Navigraph</a> - Aviation Charts (payware)', parent=self.background1)
        self.navigraph.setOpenExternalLinks(True)
        self.navigraph.setTextFormat(QtCore.Qt.RichText)
        self.navigraph.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.navigraph.setStyleSheet(linksStyle)
        self.navigraph.move(80, 160)

        self.chartFox = QLabel('•&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="https://chartfox.org/">ChartFox</a> - Aviation Charts (freeware)', parent=self.background1)
        self.chartFox.setOpenExternalLinks(True)
        self.chartFox.setTextFormat(QtCore.Qt.RichText)
        self.chartFox.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.chartFox.setStyleSheet(linksStyle)
        self.chartFox.move(80, 190)

        self.networksHeading = QLabel("Network & Maps:", parent=self.background1)
        self.networksHeading.setStyleSheet(subSubHeadingsStyle)
        self.networksHeading.move(80, 240)

        self.vatsim = QLabel('•&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="https://www.vatsim.net/">VATSIM</a> – Virtual ATC Network', parent=self.background1)
        self.vatsim.setOpenExternalLinks(True)
        self.vatsim.setTextFormat(QtCore.Qt.RichText)
        self.vatsim.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.vatsim.setStyleSheet(linksStyle)
        self.vatsim.move(80, 280)

        self.vatRadar = QLabel('•&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="https://vatsim-radar.com/">VATSIM Radar</a> - Real-time VATSIM Map', parent=self.background1)
        self.vatRadar.setOpenExternalLinks(True)
        self.vatRadar.setTextFormat(QtCore.Qt.RichText)
        self.vatRadar.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.vatRadar.setStyleSheet(linksStyle)
        self.vatRadar.move(80, 310)

        self.ivao = QLabel('•&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="https://www.ivao.aero/">IVAO</a> - Virtual ATC Network', parent=self.background1)
        self.ivao.setOpenExternalLinks(True)
        self.ivao.setTextFormat(QtCore.Qt.RichText)
        self.ivao.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.ivao.setStyleSheet(linksStyle)
        self.ivao.move(80, 340)

        self.othersHeading = QLabel("Others:", parent=self.background1)
        self.othersHeading.setStyleSheet(subSubHeadingsStyle)
        self.othersHeading.move(80, 390)

        self.noaaWeather = QLabel('•&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="https://aviationweather.gov/">NOAA</a> – Live Weather and METAR', parent=self.background1)
        self.noaaWeather.setOpenExternalLinks(True)
        self.noaaWeather.setTextFormat(QtCore.Qt.RichText)
        self.noaaWeather.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.noaaWeather.setStyleSheet(linksStyle)
        self.noaaWeather.move(80, 430)

        self.radar = QLabel('•&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="https://www.flightradar24.com/">FlightRadar24</a> - Live Flight Tracking', parent=self.background1)
        self.radar.setOpenExternalLinks(True)
        self.radar.setTextFormat(QtCore.Qt.RichText)
        self.radar.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.radar.setStyleSheet(linksStyle)
        self.radar.move(80, 460)

        self.notam = QLabel('•&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="https://notams.aim.faa.gov/notamSearch/">FAA NOTAM</a> - Notice to Air Missions Search', parent=self.background1)
        self.notam.setOpenExternalLinks(True)
        self.notam.setTextFormat(QtCore.Qt.RichText)
        self.notam.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.notam.setStyleSheet(linksStyle)
        self.notam.move(80, 490)

        self.background2=QWidget(self)
        self.background2.setFixedSize(585,595)
        self.background2.setStyleSheet("QWidget { background: rgba(255, 255, 255, 0.725); border-radius: 10px; }")
        self.background2.move(765,125)

        self.subheading2=QLabel("Pilot Card",parent=self.background2)
        self.subheading2.setStyleSheet(self.subheadingStyle)
        self.subheading2.setFixedWidth(585)
        self.subheading2.setAlignment(QtCore.Qt.AlignCenter)
        self.subheading2.move(0,30)

if __name__=="__main__":
    app = QApplication([])
    window = Misc(parent=None)
    window.show()
    appexe=app.exec()
    sys.exit(appexe)



        
