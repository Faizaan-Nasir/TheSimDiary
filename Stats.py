from clock import Clock
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
matplotlib.use('Qt5Agg')
from PyQt5.QtGui import *
import numpy as np
import os
from flight import Flight
from info import Info
from allFlights import AllFlights
from weather import Weather
from log import logBook
from misc import Misc

base_dir = os.path.dirname(__file__)
class Stats(QWidget):
    def __init__(self):
        super().__init__()
        self.airports=pd.read_csv("./src/airport-codes.csv")
        self.aircrafts=pd.read_csv("./src/ICAOList.csv", encoding='latin1')
        try:
            self.df=pd.read_csv("./src/data.csv")
        except FileNotFoundError:
            df=pd.DataFrame({"callsign":["SAMPLE"],
                "aircraft":["B738"],
                "dep":["PHOG"],
                "arr":["PHNL"],
                "time":["00:20"],
                "distance":[151],
                "date":["21/05/25"]})
            df.to_csv("./src/data.csv",index=False)
            self.df=df

        self.setWindowTitle("Pilot Diary")
        self.setFixedWidth(1400)
        self.setFixedHeight(760)
        pixmap = QPixmap(os.path.join(base_dir, 'src', 'background.jpg'))
        palette = self.palette()
        palette.setBrush(QPalette.Background, QBrush(pixmap))
        self.setPalette(palette)
        self.setWindowIcon(QtGui.QIcon('./src/icon.ico'))
        # data=urllib.request.urlopen("https://tgftp.nws.noaa.gov/data/observations/metar/stations/VABB.TXT")
        # for line in data:
        #     print(line.decode("utf-8"))

        self.setUI()
    
    def setUI(self):
        self.figure = plt.figure(figsize=(5,5))
        self.figure.patch.set_alpha(0.0)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background:transparent;")
        self.canvas.setFixedSize(500,500)

        self.heading=QLabel('The Pilot Diary',parent=self)
        self.heading.setFixedWidth(1350)
        self.heading.move(0,40)
        self.heading.setAlignment(QtCore.Qt.AlignCenter)
        self.heading.setStyleSheet("background:rgba(255, 255, 255, 0.725);font-size:45px;font-weight:800;padding:8px;margin-left:50px;border-radius:10px;color:#515151")

        self.GraphArea=QWidget(self)
        self.GraphArea.setFixedSize(600,595)
        self.GraphArea.setStyleSheet("background: rgba(255, 255, 255, 0.725); border-radius: 10px")
        self.GraphArea.move(50,125)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas, alignment=QtCore.Qt.AlignCenter)
        self.GraphArea.setLayout(layout)
        self.plot()

        self.background=QWidget(self)
        self.background.setFixedSize(400,300)
        self.background.setStyleSheet("QWidget { background: rgba(255, 255, 255, 0.725); border-radius: 10px; }")
        self.background.move(665,125)

        try:
            self.PrevFlight=Flight(self.df.loc[self.df.dep.count()-1],self.airports,self.aircrafts,parent=self.background)
        except:
            df=pd.DataFrame({"callsign":["SAMPLE"],
                "aircraft":["B738"],
                "dep":["PHOG"],
                "arr":["PHNL"],
                "time":["00:20"],
                "distance":[151],
                "date":["21/05/25"]})
            self.PrevFlight=Flight(df.iloc[0],self.airports,self.aircrafts,parent=self.background)

        self.buttonBox=QWidget(self)
        self.buttonBox.setFixedSize(270,300)
        self.buttonBox.move(1080,125)
        self.buttonBox.setStyleSheet("background: rgba(255, 255, 255, 0.725); border-radius: 10px")

        buttonStyleSheet='''QPushButton{
                                border-radius:10px;
                                color:white;
                                background:slategrey;
                                font-size:18px;
                                font-weight:400;
                            }
                            QPushButton:hover{
                                background:#656c84;
                            }'''
        
        self.showDB=QPushButton(text="All Flights",parent=self.buttonBox)
        self.showDB.move(20,20)
        self.showDB.setFixedSize(230,50)
        self.showDB.setStyleSheet(buttonStyleSheet)
        self.showDB.clicked.connect(self.openAllFlight)

        self.showLB=QPushButton(text="Log Book",parent=self.buttonBox)
        self.showLB.move(20,90)
        self.showLB.setFixedSize(230,50)
        self.showLB.setStyleSheet(buttonStyleSheet)
        self.showLB.clicked.connect(self.openLogBook)

        self.misc=QPushButton(text="Miscellaneous",parent=self.buttonBox)
        self.misc.move(20,160)
        self.misc.setFixedSize(230,50)
        self.misc.setStyleSheet(buttonStyleSheet)
        self.misc.clicked.connect(self.openMisc)

        self.showWeather=QPushButton(text="Search Weather",parent=self.buttonBox)
        self.showWeather.move(20,230)
        self.showWeather.setFixedSize(230,50)
        self.showWeather.setStyleSheet(buttonStyleSheet)
        self.showWeather.clicked.connect(self.weather)

        self.clockBox=QWidget(self)
        self.clockBox.setFixedSize(280,280)
        self.clockBox.move(665,440)
        self.clockBox.setStyleSheet("background: rgba(255, 255, 255, 0.725); border-radius: 10px")

        self.utcTime=QLabel(str(datetime.utcnow().hour)+' hrs '+str(datetime.utcnow().minute)+' mins',self.clockBox)
        self.utcTime.move(0,228)
        self.utcTime.setFixedWidth(280)
        self.utcTime.setStyleSheet("background:rgba(255, 255, 255, 0);font-size:15px;font-weight:600;color:#515151")
        self.utcTime.setAlignment(QtCore.Qt.AlignCenter)

        self.utc=Clock(parent=self.clockBox)
        self.utc.setFixedSize(150,150)
        self.utc.move(65,65)
        
        self.utcTitle=QLabel("UTC Time",self.clockBox)
        self.utcTitle.move(0,30)
        self.utcTitle.setFixedWidth(280)
        self.utcTitle.setStyleSheet("background:rgba(255, 255, 255, 0);font-size:17px;font-weight:800;color:#515151")
        self.utcTitle.setAlignment(QtCore.Qt.AlignCenter)

        self.infoBar=QWidget(self)
        self.infoBar.setFixedSize(390,280)
        self.infoBar.move(960,440)
        self.infoBar.setStyleSheet("QWidget { background: rgba(255, 255, 255, 0.725); border-radius: 10px; }")

        try:
            self.info=Info(self.airports,self.aircrafts,self.df,parent=self.infoBar)
        except:
            df=pd.DataFrame({"callsign":["SAMPLE"],
                "aircraft":["B738"],
                "dep":["PHOG"],
                "arr":["PHNL"],
                "time":["00:20"],
                "distance":[151]})
            self.info=Info(self.airports,self.aircrafts,df,parent=self.infoBar)
        self.updateTime() 
        self.updateInfo()

    def openLogBook(self):
        self.hide()
        self.logBook=logBook(parent=self)
        self.logBook.show()

    def openAllFlight(self):
        self.hide()
        self.allFlights=AllFlights(self.df,parent=self)
        self.allFlights.show()
        
    def weather(self):
        self.hide()
        self.weatherWin=Weather(self.airports,parent=self)
        self.weatherWin.show()

    def openMisc(self):
        self.hide()
        self.Win=Misc(parent=self)
        self.Win.show()

    def updateInfo(self):
        self.df=pd.read_csv("./src/data.csv")
        self.numFlights.deleteLater()
        self.numFlights=QLabel(text=str(self.df.aircraft.count()),parent=self.GraphArea)
        self.numFlights.setFixedWidth(600)
        self.numFlights.move(0,280)
        self.numFlights.setAlignment(QtCore.Qt.AlignCenter)
        self.numFlights.setStyleSheet("background:rgba(255, 255, 255, 0.0);font-size:35px;font-weight:800;border-radius:10px;color:#727272")
        self.numFlights.show()
        self.info.deleteLater()
        self.PrevFlight.deleteLater()
        try:
            self.PrevFlight=Flight(self.df.loc[self.df.dep.count()-1],self.airports,self.aircrafts,parent=self.background)
            self.info=Info(self.airports,self.aircrafts,self.df,parent=self.infoBar) 
        except:
            df=pd.DataFrame({"callsign":["SAMPLE"],
                "aircraft":["B738"],
                "dep":["PHOG"],
                "arr":["PHNL"],
                "time":["00:20"],
                "distance":[151],
                "date":["21/05/25"]})
            self.PrevFlight=Flight(df.iloc[0],self.airports,self.aircrafts,parent=self.background)
            self.info=Info(self.airports,self.aircrafts,df,parent=self.infoBar)         
        self.info.show()
        self.PrevFlight.show()
        QTimer.singleShot(10000,self.updateInfo)

    def updateTime(self):
        self.utcTime.deleteLater()
        self.utcTime=QLabel(str(datetime.utcnow().hour)+' hrs '+str(datetime.utcnow().minute)+' mins',self.clockBox)
        self.utcTime.move(0,228)
        self.utcTime.setFixedWidth(280)
        self.utcTime.setStyleSheet("background:rgba(255, 255, 255, 0);font-size:15px;font-weight:600;color:#515151")
        self.utcTime.setAlignment(QtCore.Qt.AlignCenter)
        self.utcTime.show()
        QTimer.singleShot(1000,self.updateTime)

    def plot(self):
        temp=self.df["aircraft"].value_counts()
        colors = plt.get_cmap('bone')(np.linspace(0.7,0.2, temp.count()))
        self.figure.clear()

        self.numFlights=QLabel(text=str(self.df.aircraft.count()),parent=self.GraphArea)
        self.numFlights.setFixedWidth(600)
        self.numFlights.move(0,280)
        self.numFlights.setAlignment(QtCore.Qt.AlignCenter)
        self.numFlights.setStyleSheet("background:rgba(255, 255, 255, 0.0);font-size:35px;font-weight:800;border-radius:10px;color:#727272")

        ax = self.figure.add_subplot(111)
        ax.set_position([0.1, 0.1, 0.8, 0.8])
        ax.set_aspect('equal')         
        ax.set_facecolor(None)
        ax.pie(temp,radius=1.15,colors=colors,labels=temp.index,wedgeprops={"linewidth": 1, "edgecolor": "white", 'antialiased': True,"width": 0.45},textprops={'fontsize': 12,'fontweight': 'bold', 'color': '#727272'})
        self.canvas.draw()
