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
from info import Info
from metar import Metar
import haversine as hs   
from haversine import Unit

base_dir = os.path.dirname(__file__)

class AllFlights(QWidget):
    def __init__(self,df,**kwargs):
        super().__init__(**kwargs)
        self.setWindowTitle("Pilot Diary")
        self.setFixedWidth(1400)
        self.setFixedHeight(750)
        pixmap = QPixmap(os.path.join(base_dir, 'src', 'background.jpg'))
        palette = self.palette()
        palette.setBrush(QPalette.Background, QBrush(pixmap))
        self.setPalette(palette)
        self.airports=pd.read_csv("./src/airport-codes.csv")
        self.aircrafts=pd.read_csv("./src/ICAOList.csv", encoding='latin1')
        self.df=df
        self.setWindowIcon(QtGui.QIcon('./src/icon.ico'))

        self.showUI()
    
    def showUI(self):
        self.heading=QLabel('All Flights',parent=self)
        self.heading.setFixedWidth(1350)
        self.heading.move(0,40)
        self.heading.setAlignment(QtCore.Qt.AlignCenter)
        self.heading.setStyleSheet("background:rgba(255, 255, 255, 0.725);font-size:45px;font-weight:800;padding:8px;margin-left:50px;border-radius:10px;color:#515151")

        self.background=QWidget(self)
        self.background.setFixedSize(400,300)
        self.background.setStyleSheet("QWidget { background: rgba(255, 255, 255, 0.725); border-radius: 10px; }")
        self.background.move(50,125)

        print(self.df.loc[self.df.dep.count()-1])
        self.flight=Flight(self.df.loc[self.df.dep.count()-1],self.airports,self.aircrafts,parent=self.background)

        self.tableArea=QWidget(self)
        self.tableArea.setFixedSize(885,595)
        self.tableArea.setStyleSheet("QWidget { background: rgba(255, 255, 255, 0.725); border-radius: 10px; }")
        self.tableArea.move(465,125)

        self.table=Table(self.df,parent=self.tableArea)

        headerStyle='''background:rgba(255, 255, 255, 0);font-size:18px;font-weight:800;color:#515151;border-style: solid;border-radius:0px;border-width: 0px 1px 2px 1px;border-color:#515151;'''
        
        self.cs=QLabel(text="Callsign",parent=self.tableArea)
        self.cs.setFixedSize(147,54)
        self.cs.move(2,1)
        self.cs.setStyleSheet("background:rgba(255, 255, 255, 0);font-size:18px;font-weight:800;color:#515151;border-style: solid;border-radius:0px;border-width: 0px 1px 2px 0px;border-color:#515151;")
        self.cs.setAlignment(QtCore.Qt.AlignCenter)

        self.ac=QLabel(text="Aircraft",parent=self.tableArea)
        self.ac.setFixedSize(147,54)
        self.ac.move(149,1)
        self.ac.setStyleSheet(headerStyle)
        self.ac.setAlignment(QtCore.Qt.AlignCenter)

        self.dep=QLabel(text="Departure",parent=self.tableArea)
        self.dep.setFixedSize(147,54)
        self.dep.move(296,1)
        self.dep.setStyleSheet(headerStyle)
        self.dep.setAlignment(QtCore.Qt.AlignCenter)

        self.arr=QLabel(text="Arrival",parent=self.tableArea)
        self.arr.setFixedSize(147,54)
        self.arr.move(443,1)
        self.arr.setStyleSheet(headerStyle)
        self.arr.setAlignment(QtCore.Qt.AlignCenter)

        self.time=QLabel(text="Time",parent=self.tableArea)
        self.time.setFixedSize(147,54)
        self.time.move(590,1)
        self.time.setStyleSheet(headerStyle)
        self.time.setAlignment(QtCore.Qt.AlignCenter)

        self.dist=QLabel(text="Distance",parent=self.tableArea)
        self.dist.setFixedSize(147,54)
        self.dist.move(737,1)
        self.dist.setStyleSheet("background:rgba(255, 255, 255, 0);font-size:18px;font-weight:800;color:#515151;border-style: solid;border-radius:0px;border-width: 0px 0px 2px 1px;border-color:#515151;")
        self.dist.setAlignment(QtCore.Qt.AlignCenter)

        self.searchArea=QWidget(self)
        self.searchArea.setFixedSize(400,280)
        self.searchArea.setStyleSheet("QWidget { background: rgba(255, 255, 255, 0.725); border-radius: 10px; }")
        self.searchArea.move(50,440)

        self.searchCall=QLineEdit(parent=self.searchArea)
        self.searchCall.setStyleSheet('font-size:20px;border:none;background:#A4A4A4;border-radius:10px;padding:10px;color:white;font-weight:400;')
        self.searchCall.setAlignment(QtCore.Qt.AlignCenter)
        self.searchCall.setFixedWidth(340)
        self.searchCall.move(30,25)
        self.searchCall.setPlaceholderText('by callsign')
        self.searchCall.returnPressed.connect(self.searchCallsign)

        self.searchAC=QLineEdit(parent=self.searchArea)
        self.searchAC.setStyleSheet('font-size:20px;border:none;background:#A4A4A4;border-radius:10px;padding:10px;color:white;font-weight:400;')
        self.searchAC.setAlignment(QtCore.Qt.AlignCenter)
        self.searchAC.setFixedWidth(162)
        self.searchAC.move(30,86)
        self.searchAC.setPlaceholderText('by aircraft')
        self.searchAC.returnPressed.connect(self.searchAcraft)

        self.searchAP=QLineEdit(parent=self.searchArea)
        self.searchAP.setStyleSheet('font-size:20px;border:none;background:#A4A4A4;border-radius:10px;padding:10px;color:white;font-weight:400;')
        self.searchAP.setAlignment(QtCore.Qt.AlignCenter)
        self.searchAP.setFixedWidth(162)
        self.searchAP.move(208,86)
        self.searchAP.setPlaceholderText('by airport')
        self.searchAP.returnPressed.connect(self.searchAPort)

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
        self.buttonStyleSheet=buttonStyleSheet

        self.showDB=QPushButton(text="Show All Flights",parent=self.searchArea)
        self.showDB.move(30,208)
        self.showDB.setFixedSize(340,46)
        self.showDB.setStyleSheet(buttonStyleSheet)
        self.showDB.clicked.connect(self.allFlights)

        self.newRec=QPushButton(text="New Record",parent=self.searchArea)
        self.newRec.move(30,148)
        self.newRec.setFixedSize(162,46)
        self.newRec.setStyleSheet(buttonStyleSheet)
        self.newRec.clicked.connect(self.addNewRec)

        self.delRec=QPushButton(text="Delete Record",parent=self.searchArea)
        self.delRec.move(208,148)
        self.delRec.setFixedSize(162,46)
        self.delRec.setStyleSheet(buttonStyleSheet)
        self.delRec.clicked.connect(self.delRecord)
    
    def delRecord(self):
        self.delWin=QWidget()
        self.delWin.setFixedSize(300,147)
        self.delWin.setWindowTitle("Delete Record")
        self.delWin.setWindowIcon(QtGui.QIcon('./src/icon.ico'))

        self.csEdit=QLineEdit(parent=self.delWin)
        self.csEdit.setStyleSheet('font-size:20px;border:none;background:#A4A4A4;border-radius:10px;padding:10px;color:white;font-weight:400;')
        self.csEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.csEdit.setFixedWidth(230)
        self.csEdit.move(35,20)
        self.csEdit.setPlaceholderText('callsign')
        self.csEdit.setFocusPolicy(QtCore.Qt.ClickFocus)

        self.submitDel=QPushButton(text="Submit",parent=self.delWin)
        self.submitDel.move(35,81)
        self.submitDel.setFixedSize(230,46)
        self.submitDel.setStyleSheet(self.buttonStyleSheet)
        self.submitDel.clicked.connect(self.deleteRecord)

        self.delWin.show()

    def deleteRecord(self):
        self.df=self.df[self.df.callsign!=self.csEdit.text()]
        self.df.to_csv("./src/data.csv",index=False)
        self.allFlights()
        self.delWin.deleteLater()

    def addNewRec(self):
        self.addRec=QWidget()
        self.addRec.setFixedSize(300,390)
        self.addRec.setWindowTitle("Add Record")
        self.addRec.setWindowIcon(QtGui.QIcon('./src/icon.ico'))

        self.csEdit=QLineEdit(parent=self.addRec)
        self.csEdit.setStyleSheet('font-size:20px;border:none;background:#A4A4A4;border-radius:10px;padding:10px;color:white;font-weight:400;')
        self.csEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.csEdit.setFixedWidth(230)
        self.csEdit.move(35,20)
        self.csEdit.setPlaceholderText('callsign')
        self.csEdit.setFocusPolicy(QtCore.Qt.ClickFocus)

        self.acEdit=QLineEdit(parent=self.addRec)
        self.acEdit.setStyleSheet('font-size:20px;border:none;background:#A4A4A4;border-radius:10px;padding:10px;color:white;font-weight:400;')
        self.acEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.acEdit.setFixedWidth(230)
        self.acEdit.move(35,81)
        self.acEdit.setPlaceholderText('aircraft')
        self.acEdit.setFocusPolicy(QtCore.Qt.ClickFocus)

        self.depEdit=QLineEdit(parent=self.addRec)
        self.depEdit.setStyleSheet('font-size:20px;border:none;background:#A4A4A4;border-radius:10px;padding:10px;color:white;font-weight:400;')
        self.depEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.depEdit.setFixedWidth(230)
        self.depEdit.move(35,142)
        self.depEdit.setPlaceholderText('departure')
        self.depEdit.setFocusPolicy(QtCore.Qt.ClickFocus)

        self.arrEdit=QLineEdit(parent=self.addRec)
        self.arrEdit.setStyleSheet('font-size:20px;border:none;background:#A4A4A4;border-radius:10px;padding:10px;color:white;font-weight:400;')
        self.arrEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.arrEdit.setFixedWidth(230)
        self.arrEdit.move(35,203)
        self.arrEdit.setPlaceholderText('arrival')
        self.arrEdit.setFocusPolicy(QtCore.Qt.ClickFocus)

        self.timeEdit=QLineEdit(parent=self.addRec)
        self.timeEdit.setStyleSheet('font-size:20px;border:none;background:#A4A4A4;border-radius:10px;padding:10px;color:white;font-weight:400;')
        self.timeEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.timeEdit.setFixedWidth(230)
        self.timeEdit.move(35,264)
        self.timeEdit.setPlaceholderText('airtime')
        self.timeEdit.setFocusPolicy(QtCore.Qt.ClickFocus)

        self.submitRec=QPushButton(text="Submit",parent=self.addRec)
        self.submitRec.move(35,325)
        self.submitRec.setFixedSize(230,46)
        self.submitRec.setStyleSheet(self.buttonStyleSheet)
        self.submitRec.clicked.connect(self.submitRecord)

        self.addRec.show()

    def submitRecord(self):
        try:
            print(self.aircrafts[self.aircrafts.icao==self.acEdit.text()].iloc[0])
            print(self.airports[self.airports.icao_code==self.arrEdit.text()].iloc[0])
            print(self.airports[self.airports.icao_code==self.depEdit.text()].iloc[0])
            coor1=self.airports.coordinates[self.airports.icao_code==self.depEdit.text()].iloc[0].split(',')
            coor2=self.airports.coordinates[self.airports.icao_code==self.arrEdit.text()].iloc[0].split(',')
            coor1[0]=float(coor1[0])
            coor1[1]=float(coor1[1])
            coor2[0]=float(coor2[0])
            coor2[1]=float(coor2[1])
            result=int(hs.haversine(coor1,coor2,unit=Unit.KILOMETERS))
            self.df=pd.concat([self.df,pd.DataFrame([{
                "callsign":self.csEdit.text(),
                "aircraft":self.acEdit.text(),
                "dep":self.depEdit.text(),
                "arr":self.arrEdit.text(),
                "time":self.timeEdit.text(),
                "distance":int(result)
            }])],ignore_index=True)
            self.df.to_csv("./src/data.csv",index=False)
            self.allFlights()
        except Exception as e:
            self.exception=QMessageBox.critical(self.addRec,"Error!","Incorrect entry in one or more field(s).")
        finally:
            self.addRec.deleteLater()

    def allFlights(self):
        self.flight.deleteLater()
        self.flight=Flight(self.df.loc[self.df.dep.count()-1],self.airports,self.aircrafts,parent=self.background)
        self.flight.show()
        self.searchAC.clear()
        self.searchAP.clear()
        self.searchCall.clear()
        self.table.deleteLater()
        self.table=Table(self.df,parent=self.tableArea)
        self.table.show()
        
    def searchAPort(self):
        try:
            print(self.df[(self.df.arr==self.searchAP.text()) | (self.df.dep==self.searchAP.text())].iloc[0])
            self.flight.deleteLater()
            self.flight=Flight(self.df[(self.df.arr==self.searchAP.text()) | (self.df.dep==self.searchAP.text())].iloc[0],self.airports,self.aircrafts,parent=self.background)
            self.flight.show()
            self.table.deleteLater()
            self.table=Table(self.df[(self.df.arr==self.searchAP.text()) | (self.df.dep==self.searchAP.text())],parent=self.tableArea)
            self.table.show()

        except Exception as e:
            print(e)

        finally:
            self.searchCall.clear()
            self.searchAC.clear()


    def searchCallsign(self):
        try:
            print(self.df[self.df.callsign==self.searchCall.text()].iloc[0])
            self.flight.deleteLater()
            self.flight=Flight(self.df[self.df.callsign==self.searchCall.text()].iloc[0],self.airports,self.aircrafts,parent=self.background)
            self.flight.show()
            self.table.deleteLater()
            self.table=Table(self.df[self.df.callsign==self.searchCall.text()],parent=self.tableArea)
            self.table.show()

        except Exception as e:
            print(e)
        
        finally:
            self.searchAC.clear()
            self.searchAP.clear()

    def searchAcraft(self):
        try:
            print(self.df[self.df.aircraft==self.searchAC.text()].iloc[0])
            self.flight.deleteLater()
            self.flight=Flight(self.df[self.df.aircraft==self.searchAC.text()].iloc[0],self.airports,self.aircrafts,parent=self.background)
            self.flight.show()
            self.table.deleteLater()
            self.table=Table(self.df[self.df.aircraft==self.searchAC.text()],parent=self.tableArea)
            self.table.show()

        except Exception as e:
            print(e)
        
        finally:
            self.searchAP.clear()
            self.searchCall.clear()

class Table(QTableWidget):
    def __init__(self,df,**kwargs):
        super().__init__(**kwargs)
        self.df=df
        self.setRowCount(0)      # At least 1 row for your header
        self.setColumnCount(6)   # 6 columns for your headers
        self.setFixedSize(885,540)
        self.move(2,54)
        for col in range(6):
            self.setColumnWidth(col, 147)
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.setStyleSheet('''QWidget { background: rgba(255, 255, 255, 0); border-radius: 10px; }
                                    QTableWidget::item {
                                        border-top: 1px solid #515151;
                                        border-left: 0px solid #515151;
                                        border-bottom: 0px solid #515151;
                                        border-right: none;
                                    }'''
                                 )
        self.setShowGrid(False)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        
        textStyle='''background:rgba(255, 255, 255, 0);font-size:15px;font-weight:400;color:#515151;border-right:1px solid #515151;border-left:1px solid #515151;border-radius:0px;'''

        for i in range(self.df.arr.count()-1,-1,-1):
            self.insertRow(self.rowCount())
            self.cs=QLabel(text=self.df.callsign.iloc[i])
            self.cs.setFixedSize(147,50)
            self.cs.setStyleSheet("background:rgba(255, 255, 255, 0);font-size:15px;font-weight:400;color:#515151;border-right:1px solid #515151;border-radius:0px;")
            self.cs.setAlignment(QtCore.Qt.AlignCenter)
            self.setCellWidget(self.rowCount()-1,0,(self.cs))

            self.ac=QLabel(text=self.df.aircraft.iloc[i])
            self.ac.setFixedSize(147,50)
            self.ac.setStyleSheet(textStyle)
            self.ac.setAlignment(QtCore.Qt.AlignCenter)
            self.setCellWidget(self.rowCount()-1,1,(self.ac))

            self.dep=QLabel(text=self.df.dep.iloc[i])
            self.dep.setFixedSize(147,50)
            self.dep.setStyleSheet(textStyle)
            self.dep.setAlignment(QtCore.Qt.AlignCenter)
            self.setCellWidget(self.rowCount()-1,2,self.dep)

            self.arr=QLabel(text=self.df.arr.iloc[i])
            self.arr.setFixedSize(147,50)
            self.arr.setStyleSheet(textStyle)
            self.arr.setAlignment(QtCore.Qt.AlignCenter)
            self.setCellWidget(self.rowCount()-1,3,self.arr)

            self.time=QLabel(text=self.df.time.iloc[i])
            self.time.setFixedSize(147,50)
            self.time.setStyleSheet(textStyle)
            self.time.setAlignment(QtCore.Qt.AlignCenter)
            self.setCellWidget(self.rowCount()-1,4,self.time)

            self.dist=QLabel(text=str(self.df.distance.iloc[i]))
            self.dist.setFixedSize(147,50)
            self.dist.setStyleSheet("background:rgba(255, 255, 255, 0);font-size:15px;font-weight:400;color:#515151;border-left:1px solid #515151;border-radius:0px;")
            self.dist.setAlignment(QtCore.Qt.AlignCenter)
            self.setCellWidget(self.rowCount()-1,5,self.dist)

if __name__=="__main__":
    df=pd.read_csv("./src/data.csv")
    app = QApplication([])
    window = AllFlights(df)
    window.show()
    appexe=app.exec()
    sys.exit(appexe)
