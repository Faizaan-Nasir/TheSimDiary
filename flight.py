from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5.QtGui import *

class Flight(QWidget):
    def __init__(self,df,airports,aircrafts,**kwargs):
        super().__init__(**kwargs)
        self.df=df
        # print(type(df))
        self.airports=airports
        self.aircrafts=aircrafts
        self.setFixedSize(400,300)

        self.PrevFileTitle=QLabel(text=f"{self.df.callsign}",parent=self)
        self.PrevFileTitle.setStyleSheet("background:rgba(255, 255, 255, 0.0);font-size:30px;font-weight:600;color:#515151")
        self.PrevFileTitle.setFixedWidth(400)
        self.PrevFileTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.PrevFileTitle.move(0,40)

        self.image = QLabel(parent=self)
        pixmap = QPixmap('src/airplance-icon.png')  # Replace with your image path
        self.image.setPixmap(pixmap)
        self.image.move(0,100)
        self.image.setFixedWidth(400)
        self.image.setAlignment(QtCore.Qt.AlignCenter)
        self.image.setStyleSheet("background:rgba(0,0,0,0)")

        # print(self.df)
        self.origin=QLabel(text=f"{self.df.dep}",parent=self)
        self.origin.move(10,135)
        self.origin.setFixedWidth(160)
        self.origin.setAlignment(QtCore.Qt.AlignCenter)
        self.origin.setStyleSheet("background:rgba(255, 255, 255, 0);font-size:20px;font-weight:800;color:#515151")

        self.originName=QLabel(text=f"({self.airports.iata_code[self.airports.icao_code == self.df.dep].iloc[0]})",parent=self)
        self.originName.setWordWrap(True)
        self.originName.move(10,165)
        self.originName.setFixedWidth(160)
        self.originName.setAlignment(QtCore.Qt.AlignCenter)
        self.originName.setStyleSheet("background:rgba(255, 255, 255, 0);font-size:15px;font-weight:800;color:#515151")

        self.dest=QLabel(text=f"{self.df.arr}",parent=self)
        self.dest.move(230,135)
        self.dest.setFixedWidth(160)
        self.dest.setAlignment(QtCore.Qt.AlignCenter)
        self.dest.setStyleSheet("background:rgba(255, 255, 255, 0);font-size:20px;font-weight:800;color:#515151")

        self.destName=QLabel(text=f"({self.airports.iata_code[self.airports.icao_code == self.df.arr].iloc[0]})",parent=self)
        self.destName.setWordWrap(True)
        self.destName.move(230,165)
        self.destName.setFixedWidth(160)
        self.destName.setAlignment(QtCore.Qt.AlignCenter)
        self.destName.setStyleSheet("background:rgba(255, 255, 255, 0);font-size:15px;font-weight:800;color:#515151")

        dftime=self.df.time
        self.time=QLabel(text=f"({dftime[:dftime.find(':')]} hrs {dftime[dftime.find(':')+1:]} mins)",parent=self)
        self.time.move(0,212)
        self.time.setFixedWidth(400)
        self.time.setAlignment(QtCore.Qt.AlignCenter)
        self.time.setStyleSheet("background:rgba(255, 255, 255, 0);font-size:18px;font-weight:400;color:#515151")

        
        aircraft_name = self.aircrafts.name[self.aircrafts.icao == self.df.aircraft].iloc[0]
        self.aircraftType = QLabel(text=aircraft_name, parent=self)
        self.aircraftType.setFixedWidth(400)
        self.aircraftType.move(0,240)
        self.aircraftType.setAlignment(QtCore.Qt.AlignCenter)
        self.aircraftType.setStyleSheet("background:rgba(255, 255, 255, 0);font-size:22px;font-weight:800;color:#515151")