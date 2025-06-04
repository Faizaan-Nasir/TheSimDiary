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
from datetime import datetime
from clock import Clock
from PyQt5.QtCore import QTimer
from comprehendWeather import giveWeather
from comprehendWeather import giveTime

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
        self.backdrop.setFixedSize(1005,595)
        self.backdrop.move(50,125)

        self.searchBar=QLineEdit(parent=self.backdrop)
        self.searchBar.setStyleSheet('font-size:20px;border:none;background:#A4A4A4;border-radius:10px;padding:10px;color:white;font-weight:400;')
        self.searchBar.setFixedWidth(705)
        self.searchBar.move(50,40)
        self.searchBar.setPlaceholderText('search airport by icao')
        self.searchBar.setText("PHNL")
        self.searchBar.returnPressed.connect(self.search)

        self.submit=QPushButton("Search",parent=self.backdrop)
        self.submit.setFixedSize(185,45)
        self.submit.setStyleSheet('''QPushButton{
                                        border-radius:10px;
                                        color:white;
                                        background:slategrey;
                                        font-size:20px;
                                        font-weight:400;
                                    }
                                    QPushButton:hover{
                                        background:#656c84;
                                    }''')
        self.submit.move(770,40)
        self.submit.clicked.connect(self.search)

        self.raw=QLabel("\n",parent=self.backdrop)
        self.raw.setStyleSheet("background:rgba(255, 255, 255, 0.0);font-size:15px;font-weight:400;color:#515151;border-radius:10px;padding:10px")
        self.raw.move(50,95)
        self.raw.setFixedWidth(905)
        self.raw.setWordWrap(True)
        self.raw.setAlignment(QtCore.Qt.AlignCenter)

        self.metar=QWidget(parent=self)
        self.metar.setStyleSheet("background:rgba(255, 255, 255, 0.0);font-size:22px;font-weight:400;color:#515151;border-radius:10px;padding:10px")
        self.metar.move(100,275)
        # self.metar.setWordWrap(True)
        self.metar.setFixedWidth(805)
        # self.metar.setAlignment(QtCore.Qt.AlignCenter)

        self.clockBox=QWidget(self)
        self.clockBox.setFixedSize(280,280)
        self.clockBox.move(1070,125)
        self.clockBox.setStyleSheet("background: rgba(255, 255, 255, 0.725); border-radius: 10px")

        self.utcTime=QLabel(str(datetime.utcnow().hour)+' hrs '+str(datetime.utcnow().minute)+' mins',self.clockBox)
        self.utcTime.move(0,228)
        self.utcTime.setFixedWidth(280)
        self.utcTime.setStyleSheet("background:rgba(255, 255, 255, 0);font-size:15px;font-weight:600;color:#515151")
        self.utcTime.setAlignment(QtCore.Qt.AlignCenter)

        self.utc=Clock(parent=self.clockBox)
        self.utc.setFixedSize(150,150)
        self.utc.move(65,65)
        
        self.utcTitle=QLabel("<u>UTC Time</u>",self.clockBox)
        self.utcTitle.move(0,28)
        self.utcTitle.setFixedWidth(280)
        self.utcTitle.setStyleSheet("background:rgba(255, 255, 255, 0);font-size:23px;font-weight:800;color:#515151")
        self.utcTitle.setAlignment(QtCore.Qt.AlignCenter)

        self.infoBg=QWidget(parent=self)
        self.infoBg.move(1070,420)
        self.infoBg.setFixedSize(280,300)
        self.infoBg.setStyleSheet("background: rgba(255, 255, 255, 0.725); border-radius: 10px")

        self.infoTitle=QLabel("<u>Additional Info</u>",self.infoBg)
        self.infoTitle.move(0,30)
        self.infoTitle.setFixedWidth(280)
        self.infoTitle.setStyleSheet("background:rgba(255, 255, 255, 0);font-size:23px;font-weight:800;color:#515151")
        self.infoTitle.setAlignment(QtCore.Qt.AlignCenter)

        self.infostyle="background:rgba(255, 255, 255, 0);font-size:18px;font-weight:400;color:#515151"
        self.infoTitleStyle="background:rgba(255, 255, 255, 0);font-size:18px;font-weight:600;color:#515151"
        
        self.cityTitle=QLabel("City: ",self.infoBg)
        self.cityTitle.move(30,75)
        self.cityTitle.setStyleSheet(self.infoTitleStyle)
        self.cityTitle.setFixedWidth(220)

        self.city=QLabel("",self.infoBg)
        self.city.move(30,75)
        self.city.setStyleSheet(self.infostyle)
        self.city.setFixedWidth(220)
        self.city.setAlignment(QtCore.Qt.AlignRight)

        self.metarTimeTitle=QLabel("METAR Time: ",self.infoBg)
        self.metarTimeTitle.move(30,110)
        self.metarTimeTitle.setStyleSheet(self.infoTitleStyle)
        self.metarTimeTitle.setFixedWidth(220)

        self.metarTime=QLabel("",self.infoBg)
        self.metarTime.move(30,110)
        self.metarTime.setStyleSheet(self.infostyle)
        self.metarTime.setFixedWidth(220)
        self.metarTime.setAlignment(QtCore.Qt.AlignRight)

        self.elevationTitle=QLabel("Elevation: ",self.infoBg)
        self.elevationTitle.move(30,145)
        self.elevationTitle.setStyleSheet(self.infoTitleStyle)
        self.elevationTitle.setFixedWidth(220)

        self.elevation=QLabel("",self.infoBg)
        self.elevation.move(30,145)
        self.elevation.setStyleSheet(self.infostyle)
        self.elevation.setFixedWidth(220)
        self.elevation.setAlignment(QtCore.Qt.AlignRight)

        self.creditsTitle=QLabel("Source: ",self.infoBg)
        self.creditsTitle.move(30,180)
        self.creditsTitle.setStyleSheet(self.infoTitleStyle)
        self.creditsTitle.setWordWrap(True)
        self.creditsTitle.setFixedWidth(220)

        self.credits=QLabel("NOAA Weather",self.infoBg)
        self.credits.move(30,180)
        self.credits.setStyleSheet(self.infostyle)
        self.credits.setFixedWidth(220)
        self.credits.setAlignment(QtCore.Qt.AlignRight)

        self.disclaimer=QLabel('''Summarized METAR data may exclude some information from raw METAR''',self.infoBg)
        self.disclaimer.move(30,215)
        self.disclaimer.setStyleSheet("background:rgba(255, 255, 255, 0);font-size:15px;font-weight:400;color:#515151")
        self.disclaimer.setFixedWidth(220)
        self.disclaimer.setWordWrap(True)
        self.disclaimer.setAlignment(QtCore.Qt.AlignCenter)

        self.search()
        self.updateTime()


    def search(self):
        self.city.clear()
        self.metarTime.clear()
        self.elevation.clear()
        try:
            self.city.setText(self.airports.municipality[self.airports.icao_code==self.searchBar.text().upper()].iloc[0])
            # self.aerodrome.deleteLater()
            self.elevation.setText(str(self.airports.elevation_ft[self.airports.icao_code==self.searchBar.text().upper()].iloc[0])+" ft")
            # self.aerodrome=QLabel(str(self.airports.name[self.airports.icao_code==self.searchBar.text().upper()].iloc[0]),self.infoBg)
            # self.aerodrome.move(10,200)
            # self.aerodrome.setStyleSheet("background:rgba(255, 255, 255, 0);font-size:20px;font-weight:600;color:#515151")
            # self.aerodrome.setWordWrap(True)
            # self.aerodrome.setFixedWidth(260)
            # self.aerodrome.setAlignment(QtCore.Qt.AlignCenter)
            # self.aerodrome.show()
            # self.icao.setText(self.airports.name[self.airports.icao_code==self.searchBar.text().upper()].iloc[0]+" METAR")
            # self.adEle.setText("Airport Elevation: "+str(int(self.airports.elevation_ft[self.airports.icao_code==self.searchBar.text().upper()].iloc[0]))+" ft")
        except Exception as e:
            self.exception = QMessageBox.critical(self, "Not Found Error", "No airport with given ICAO") 
            print(e)
        else:
            try:
                data=urllib.request.urlopen(f"https://tgftp.nws.noaa.gov/data/observations/metar/stations/{self.searchBar.text().upper()}.TXT")
                text=""
                for line in data:
                    text+=line.decode("utf-8")
                text=text.split('\n')[1]
                # print(Metar.Metar(text.split("\n")[1]).sky)
                try:
                    giveWeather(text)
                except Exception as e:
                    self.exception = QMessageBox.critical(self, "Format Error", "The provided METAR (by NOAA) is unconventionally formatted.\nRaw METAR: "+text) 
                else:
                    self.raw.clear()
                    self.raw.setText(text)
                    self.metar.deleteLater()
                    self.metar=Table(giveWeather(text),parent=self.backdrop)
                    self.metar.move(50,150)
                    self.metar.show()
                    self.metarTime.setText(str(giveTime(text)))
            except Exception as e:
                print(e)
                self.exception = QMessageBox.critical(self, "Network Error", "Server Timeout. We could not fetch the current weather for you. Please check your internet connection.") 
                
    
    def updateTime(self):
        self.utcTime.deleteLater()
        self.utcTime=QLabel(str(datetime.utcnow().hour)+' hrs '+str(datetime.utcnow().minute)+' mins',self.clockBox)
        self.utcTime.move(0,228)
        self.utcTime.setFixedWidth(280)
        self.utcTime.setStyleSheet("background:rgba(255, 255, 255, 0);font-size:15px;font-weight:600;color:#515151")
        self.utcTime.setAlignment(QtCore.Qt.AlignCenter)
        self.utcTime.show()
        QTimer.singleShot(1000,self.updateTime)


class Table(QTableWidget):
    def __init__(self,text,**kwargs):
        super().__init__(**kwargs)
        self.text=text
        text=text.split("| ")
        self.setRowCount(1)      # At least 1 row for your header
        self.setColumnCount(2)   # 7 columns for your headers
        self.setFixedSize(905,50*len(text))
        self.move(2,54)
        self.setColumnWidth(0, 125)
        self.setColumnWidth(1,780)
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.setStyleSheet('''QWidget { background: rgba(255, 255, 255, 0); border-radius: 10px; }
                                    QTableWidget::item {
                                        border-top: 1px solid #515151;
                                        border-left: 1px solid #515151;
                                        border-bottom: 1px solid #515151;
                                        border-right: 1px solid #515151;
                                    }'''
                                 )
        self.setShowGrid(False)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        

        for i in range(len(text)):
            # print(text[i].split(": "))
            self.insertRow(i+1)
            self.title=QLabel(text[i].split(': ')[0])
            self.title.setFixedSize(125,50)
            self.title.setStyleSheet("background:rgba(255, 255, 255, 0);font-size:15px;font-weight:600;color:#515151;border-radius:0px;")
            self.title.setAlignment(QtCore.Qt.AlignCenter)
            self.setCellWidget(i,0,(self.title))

            self.info=QLabel(text[i].split(': ')[1])
            self.info.setFixedSize(780,50)
            self.info.setStyleSheet("background:rgba(255, 255, 255, 0);font-size:15px;font-weight:400;color:#515151;border-radius:0px;")
            self.info.setAlignment(QtCore.Qt.AlignCenter)
            self.info.setWordWrap(True)
            self.setCellWidget(i,1,(self.info))

        
        for i in range(self.rowCount()):
            self.setRowHeight(i,50)

        self.setVerticalScrollMode(QTableWidget.ScrollPerPixel)  # optional
        self.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)  # optional

        # Override the wheelEvent
        self.wheelEvent = lambda event: None


if __name__=="__main__":
    airports=pd.read_csv("./src/airport-codes.csv")
    app = QApplication([])
    # window = Weather(airports)
    data=urllib.request.urlopen(f"https://tgftp.nws.noaa.gov/data/observations/metar/stations/VABB.TXT")
    text=""
    for line in data:
        text+=line.decode("utf-8")
    text=text.split('\n')[1]
    # print(Metar.Metar(text.split("\n")[1]).sky)
    
    a=giveWeather(text)
    window=Table(a)
    window.show()
    appexe=app.exec()
    sys.exit(appexe)

