import sys
import urllib.request
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import QtGui
import pandas as pd
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
matplotlib.use('Qt5Agg')
from PyQt5.QtGui import *
import os
import urllib

base_dir = os.path.dirname(__file__)

class Weather(QWidget):
    def __init__(self,airports,parent,**kwargs):
        super().__init__(**kwargs)
        self.airports=airports
        self.setWindowTitle("Pilot Diary")
        self.setFixedWidth(1400)
        self.parent=parent
        self.setFixedHeight(760)
        pixmap = QPixmap(os.path.join(base_dir, 'src', 'background.jpg'))
        palette = self.palette()
        palette.setBrush(QPalette.Background, QBrush(pixmap))
        self.setPalette(palette)
        self.setWindowIcon(QtGui.QIcon('./src/icon.ico'))
        # data=urllib.request.urlopen("https://tgftp.nws.noaa.gov/data/observations/metar/stations/VABB.TXT")
        # for line in data:
        #     print(line.decode("utf-8"))

        self.showUI()

    def funGoBack(self):
        self.parent.show()
        self.close()

    def showUI(self):
        self.heading=QLabel('Search Weather',parent=self)
        self.heading.setFixedWidth(1350)
        self.heading.move(0,40)
        self.heading.setAlignment(QtCore.Qt.AlignCenter)
        self.heading.setStyleSheet("background:rgba(255, 255, 255, 0.725);font-size:45px;font-weight:800;padding:8px;margin-left:50px;border-radius:10px;color:#515151")

        self.goBack=QPushButton("< Go Back",parent=self)
        self.goBack.move(80,57)
        self.goBack.setStyleSheet("background:transparent;font-size:18px;font-weight:800;color:#515151")
        self.goBack.clicked.connect(self.funGoBack)

        self.backdrop=QWidget(parent=self)
        self.backdrop.setStyleSheet("QWidget { background: rgba(255, 255, 255, 0.725); border-radius: 10px; }")
        self.backdrop.setFixedSize(1300,595)
        self.backdrop.move(50,125)

        self.searchBar=QLineEdit(parent=self.backdrop)
        self.searchBar.setStyleSheet('font-size:25px;border:none;background:#A4A4A4;border-radius:10px;padding:10px;color:white;font-weight:400;')
        self.searchBar.setFixedWidth(550)
        self.searchBar.move(275,100)
        self.searchBar.setPlaceholderText('search airport by icao')
        self.searchBar.returnPressed.connect(self.search)

        self.submit=QPushButton("Search",parent=self.backdrop)
        self.submit.setFixedSize(185,52)
        self.submit.setStyleSheet('''QPushButton{
                                        border-radius:10px;
                                        color:white;
                                        background:slategrey;
                                        font-size:22px;
                                        font-weight:400;
                                    }
                                    QPushButton:hover{
                                        background:#656c84;
                                    }''')
        self.submit.move(840,100)
        self.submit.clicked.connect(self.search)

        self.icao=QLabel("",parent=self.backdrop)
        self.icao.setStyleSheet("background:rgba(255, 255, 255, 0.0);font-size:28px;font-weight:600;color:#515151;border-radius:10px;")
        self.icao.move(0,230)
        self.icao.setAlignment(QtCore.Qt.AlignCenter)
        self.icao.setFixedWidth(1300)

        self.metar=QLabel("\n\n\n",parent=self.backdrop)
        self.metar.setStyleSheet("background:rgba(255, 255, 255, 0.0);font-size:28px;font-weight:400;color:#515151;border-radius:10px;padding:10px")
        self.metar.move(150,275)
        self.metar.setWordWrap(True)
        self.metar.setFixedWidth(1000)
        self.metar.setAlignment(QtCore.Qt.AlignCenter)

        self.adEle=QLabel("",parent=self.backdrop)
        self.adEle.setStyleSheet("background:rgba(255, 255, 255, 0.0);font-size:28px;font-weight:600;color:#515151;border-radius:10px;")
        self.adEle.move(0,410)
        self.adEle.setAlignment(QtCore.Qt.AlignCenter)
        self.adEle.setFixedWidth(1300)

    def search(self):
        self.icao.clear()
        self.metar.clear()
        self.adEle.clear()
        try:
            self.icao.setText(self.airports.name[self.airports.icao_code==self.searchBar.text().upper()].iloc[0]+" METAR")
            self.adEle.setText("Airport Elevation: "+str(int(self.airports.elevation_ft[self.airports.icao_code==self.searchBar.text().upper()].iloc[0]))+" ft")
        except Exception as e:
            self.icao.setText("No airport with given ICAO.")
            print(e)
        else:
            try:
                data=urllib.request.urlopen(f"https://tgftp.nws.noaa.gov/data/observations/metar/stations/{self.searchBar.text().upper()}.TXT")
                text=""
                for line in data:
                    text+=line.decode("utf-8")
                # print(Metar.Metar(text.split("\n")[1]).sky)
                self.metar.setText(text)
            except Exception as e:
                msg = QMessageBox()
                msg.setWindowTitle("Network Error")
                msg.setText("Server Timeout. We could not fetch the current weather for you. Please check your internet connection.")
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
                self.metar.setText("Server Timeout. No results found")
                print(e)
if __name__=="__main__":
    airports=pd.read_csv("./src/airport-codes.csv")
    app = QApplication([])
    window = Weather(airports)
    window.show()
    appexe=app.exec()
    sys.exit(appexe)

