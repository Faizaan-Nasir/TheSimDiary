import sys
import urllib.request
from clock import Clock
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer
import mysql.connector as sql
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
matplotlib.use('Qt5Agg')
from PyQt5.QtGui import *
import numpy as np
import random
import os
import urllib
from flight import Flight

class Info(QWidget):
    def __init__(self,airports,aircrafts,df,**kwargs):
        super().__init__(**kwargs)
        self.airports=airports
        self.aircrafts=aircrafts
        self.setFixedSize(390,280)
        self.df=df
        self.setUI()
    def setUI(self):
        self.infoTitle=QLabel(text="<u>Info Hub</u>",parent=self)
        self.infoTitle.setFixedWidth(390)
        self.infoTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.infoTitle.move(0,25)
        self.infoTitle.setStyleSheet("background:rgba(255, 255, 255, 0);font-size:25px;font-weight:800;color:#515151")

        self.infoLabel=QLabel('''
                         <p>Hours Flown: </p>
                         <p>Distance Flown:</p>
                         <p>Popular Destination: </p>
                         <p>Average Flight Duration: </p>
                         <p>Frequent Fly: </p>'''
                         ,parent=self)
        self.infoLabel.move(20,78)
        self.infoLabel.setStyleSheet("background:rgba(255, 255, 255, 0);font-size:20px;font-weight:600;color:#515151")

        # cur.execute('select * from flights;')
        newdata=self.df
        nofl=len(newdata)
        tot=0
        hours=0
        mins=0
        for i in self.df.index:
            # print(self.df.loc[i]["distance"])
            tot+=int(self.df.loc[i]["distance"])
            hours+=int(self.df.loc[i]["time"][0:self.df.loc[i]["time"].find(":")])
            mins+=int(self.df.loc[i]["time"][self.df.loc[i]["time"].find(":")+1:])
        if mins>=60:
            hours+=mins//60
            mins=mins%60
        df=str(tot)
        fh=str(hours)+' hrs '+str(mins)+' mins'

        self.info=QLabel(text=f'''
                    <p>{fh}</p>
                    <p>{df} km</p>
                    <p>{self.airports.municipality[self.airports.icao_code==self.df.arr.mode().iloc[0]].iloc[0]}</p>
                    <p>{str(int(hours/self.df.callsign.count()))} hrs</p>
                    <p>{self.aircrafts.name[self.aircrafts.icao==self.df.aircraft.mode().iloc[0]].iloc[0]}</p>'''
                    ,parent=self)
        self.info.move(20,78)
        self.info.setFixedWidth(350)
        self.info.setAlignment(QtCore.Qt.AlignRight)
        self.info.setStyleSheet("background:rgba(255, 255, 255, 0);font-size:20px;font-weight:400;color:#515151")     
