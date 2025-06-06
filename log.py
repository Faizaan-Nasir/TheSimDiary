import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import QtGui
import pandas as pd
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5.QtGui import *
import os
from flight import Flight


base_dir = os.path.dirname(__file__)

class logBook(QWidget):
    def __init__(self,parent,**kwargs):
        super().__init__(**kwargs)
        self.setWindowTitle("Pilot Diary")
        self.parent=parent
        self.setFixedWidth(1400)
        self.setFixedHeight(760)
        pixmap = QPixmap(os.path.join(base_dir, 'src', 'background.jpg'))
        palette = self.palette()
        palette.setBrush(QPalette.Background, QBrush(pixmap))
        self.setPalette(palette)
        self.airports=pd.read_csv("./src/airport-codes.csv")
        self.aircrafts=pd.read_csv("./src/ICAOList.csv", encoding='latin1')
        try:
            self.df=pd.read_csv("./src/log.csv")
        except:
            df=pd.DataFrame({
                "date":["27/08/2025"],
                "mod":["iFly B38M"],
                "failure_type":["Simulated"],
                "status":["Inactive"],
                "sim":["MSFS2020"],
                "callsign":["SAMPLE"]})
            df.to_csv("./src/log.csv",index=False)
            self.df=df
        self.data=pd.read_csv("./src/data.csv")
        self.setWindowIcon(QtGui.QIcon('./src/icon.ico'))

        self.showUI()
    
    def funGoBack(self):
        self.parent.show()
        self.close()

    def showUI(self):
        self.heading=QLabel('Log Book',parent=self)
        self.heading.setFixedWidth(1350)
        self.heading.move(0,40)
        self.heading.setAlignment(QtCore.Qt.AlignCenter)
        self.heading.setStyleSheet("background:rgba(255, 255, 255, 0.725);font-size:45px;font-weight:800;padding:8px;margin-left:50px;border-radius:10px;color:#515151")

        self.goBack=QPushButton("< Go Back",parent=self)
        self.goBack.move(80,57)
        self.goBack.setStyleSheet("background:transparent;font-size:18px;font-weight:800;color:#515151")
        self.goBack.clicked.connect(self.funGoBack)

        self.background=QWidget(self)
        self.background.setFixedSize(400,300)
        self.background.setStyleSheet("QWidget { background: rgba(255, 255, 255, 0.725); border-radius: 10px; }")
        self.background.move(50,125)

        try:
            self.flight=Flight(self.data[self.data.callsign==self.df.callsign.loc[self.df.callsign.count()-1]].iloc[0],self.airports,self.aircrafts,parent=self.background)
        except:
            self.temp=pd.DataFrame({"callsign":["SAMPLE"],
                "aircraft":["B738"],
                "dep":["PHOG"],
                "arr":["PHNL"],
                "time":["00:20"],
                "distance":[151]})
            
            self.flight=Flight(self.temp.iloc[0],self.airports,self.aircrafts,parent=self.background)
        self.tableArea=QWidget(self)
        self.tableArea.setFixedSize(885,595)
        self.tableArea.setStyleSheet("QWidget { background: rgba(255, 255, 255, 0.725); border-radius: 10px; }")
        self.tableArea.move(465,125)

        self.table=Table(self.df,parent=self.tableArea)

        headerStyle='''background:rgba(255, 255, 255, 0);font-size:18px;font-weight:800;color:#515151;border-style: solid;border-radius:0px;border-width: 0px 1px 2px 1px;border-color:#515151;'''
        
        self.date=QLabel(text="Date",parent=self.tableArea)
        self.date.setFixedSize(147,54)
        self.date.move(2,1)
        self.date.setStyleSheet("background:rgba(255, 255, 255, 0);font-size:18px;font-weight:800;color:#515151;border-style: solid;border-radius:0px;border-width: 0px 1px 2px 0px;border-color:#515151;")
        self.date.setAlignment(QtCore.Qt.AlignCenter)

        self.mod=QLabel(text="Mod",parent=self.tableArea)
        self.mod.setFixedSize(147,54)
        self.mod.move(149,1)
        self.mod.setStyleSheet(headerStyle)
        self.mod.setAlignment(QtCore.Qt.AlignCenter)

        self.type=QLabel(text="Description",parent=self.tableArea)
        self.type.setFixedSize(147,54)
        self.type.move(296,1)
        self.type.setStyleSheet(headerStyle)
        self.type.setAlignment(QtCore.Qt.AlignCenter)

        self.status=QLabel(text="Status",parent=self.tableArea)
        self.status.setFixedSize(147,54)
        self.status.move(443,1)
        self.status.setStyleSheet(headerStyle)
        self.status.setAlignment(QtCore.Qt.AlignCenter)

        self.sim=QLabel(text="Simulator",parent=self.tableArea)
        self.sim.setFixedSize(147,54)
        self.sim.move(590,1)
        self.sim.setStyleSheet(headerStyle)
        self.sim.setAlignment(QtCore.Qt.AlignCenter)

        self.cs=QLabel(text="Callsign",parent=self.tableArea)
        self.cs.setFixedSize(147,54)
        self.cs.move(737,1)
        self.cs.setStyleSheet("background:rgba(255, 255, 255, 0);font-size:18px;font-weight:800;color:#515151;border-style: solid;border-radius:0px;border-width: 0px 0px 2px 1px;border-color:#515151;")
        self.cs.setAlignment(QtCore.Qt.AlignCenter)

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

        self.searchMod=QLineEdit(parent=self.searchArea)
        self.searchMod.setStyleSheet('font-size:20px;border:none;background:#A4A4A4;border-radius:10px;padding:10px;color:white;font-weight:400;')
        self.searchMod.setAlignment(QtCore.Qt.AlignCenter)
        self.searchMod.setFixedWidth(162)
        self.searchMod.move(30,86)
        self.searchMod.setPlaceholderText('by mod')
        self.searchMod.returnPressed.connect(self.byMod)

        self.searchStatus=QLineEdit(parent=self.searchArea)
        self.searchStatus.setStyleSheet('font-size:20px;border:none;background:#A4A4A4;border-radius:10px;padding:10px;color:white;font-weight:400;')
        self.searchStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.searchStatus.setFixedWidth(162)
        self.searchStatus.move(208,86)
        self.searchStatus.setPlaceholderText('by status')
        self.searchStatus.returnPressed.connect(self.byStatus)

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

        self.showDB=QPushButton(text="Show All Records",parent=self.searchArea)
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
        self.df=self.df[self.df.callsign!=self.csEdit.text().upper()]
        self.df.to_csv("./src/log.csv",index=False)
        self.allFlights()
        self.delWin.deleteLater()

    def addNewRec(self):
        self.addRec=QWidget()
        self.addRec.setFixedSize(300,450)
        self.addRec.setWindowTitle("Add Record")
        self.addRec.setWindowIcon(QtGui.QIcon('./src/icon.ico'))

        self.dateEdit=QLineEdit(parent=self.addRec)
        self.dateEdit.setStyleSheet('font-size:20px;border:none;background:#A4A4A4;border-radius:10px;padding:10px;color:white;font-weight:400;')
        self.dateEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.dateEdit.setFixedWidth(230)
        self.dateEdit.move(35,20)
        self.dateEdit.setPlaceholderText('date')
        self.dateEdit.setFocusPolicy(QtCore.Qt.ClickFocus)
        from datetime import date
        today = date.today().strftime("%d/%m/%Y")
        self.dateEdit.setText(today)

        self.modEdit=QLineEdit(parent=self.addRec)
        self.modEdit.setStyleSheet('font-size:20px;border:none;background:#A4A4A4;border-radius:10px;padding:10px;color:white;font-weight:400;')
        self.modEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.modEdit.setFixedWidth(230)
        self.modEdit.move(35,81)
        self.modEdit.setPlaceholderText('mod')
        self.modEdit.setFocusPolicy(QtCore.Qt.ClickFocus)

        self.ftEdit=QLineEdit(parent=self.addRec)
        self.ftEdit.setStyleSheet('font-size:20px;border:none;background:#A4A4A4;border-radius:10px;padding:10px;color:white;font-weight:400;')
        self.ftEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.ftEdit.setFixedWidth(230)
        self.ftEdit.move(35,142)
        self.ftEdit.setPlaceholderText('failure description')
        self.ftEdit.setFocusPolicy(QtCore.Qt.ClickFocus)

        self.statusEdit=QLineEdit(parent=self.addRec)
        self.statusEdit.setStyleSheet('font-size:20px;border:none;background:#A4A4A4;border-radius:10px;padding:10px;color:white;font-weight:400;')
        self.statusEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.statusEdit.setFixedWidth(230)
        self.statusEdit.move(35,203)
        self.statusEdit.setPlaceholderText('status')
        self.statusEdit.setFocusPolicy(QtCore.Qt.ClickFocus)

        self.simEdit=QLineEdit(parent=self.addRec)
        self.simEdit.setStyleSheet('font-size:20px;border:none;background:#A4A4A4;border-radius:10px;padding:10px;color:white;font-weight:400;')
        self.simEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.simEdit.setFixedWidth(230)
        self.simEdit.move(35,264)
        self.simEdit.setPlaceholderText('simulator')
        self.simEdit.setFocusPolicy(QtCore.Qt.ClickFocus)

        self.csEdit=QLineEdit(parent=self.addRec)
        self.csEdit.setStyleSheet('font-size:20px;border:none;background:#A4A4A4;border-radius:10px;padding:10px;color:white;font-weight:400;')
        self.csEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.csEdit.setFixedWidth(230)
        self.csEdit.move(35,325)
        self.csEdit.setPlaceholderText('callsign')
        self.csEdit.setFocusPolicy(QtCore.Qt.ClickFocus)

        self.submitRec=QPushButton(text="Submit",parent=self.addRec)
        self.submitRec.move(35,386)
        self.submitRec.setFixedSize(230,46)
        self.submitRec.setStyleSheet(self.buttonStyleSheet)
        self.submitRec.clicked.connect(self.submitRecord)

        self.addRec.show()

    def _validateDate(self) :
        from datetime import datetime
        datetime.strptime(self.dateEdit.text(), "%d/%m/%Y")

    def submitRecord(self):
        try:
            # print(self.aircrafts[self.aircrafts.icao==self.acEdit.text()].iloc[0])
            # print(self.airports[self.airports.icao_code==self.arrEdit.text()].iloc[0])
            # print(self.airports[self.airports.icao_code==self.depEdit.text()].iloc[0])
            # coor1=self.airports.coordinates[self.airports.icao_code==self.depEdit.text()].iloc[0].split(',')
            # coor2=self.airports.coordinates[self.airports.icao_code==self.arrEdit.text()].iloc[0].split(',')
            # coor1[0]=float(coor1[0])
            # coor1[1]=float(coor1[1])
            # coor2[0]=float(coor2[0])
            # coor2[1]=float(coor2[1])
            # result=int(hs.haversine(coor1,coor2,unit=Unit.KILOMETERS))
            self._validateDate()
            self.df=pd.concat([self.df,pd.DataFrame([{
                "date":self.dateEdit.text(),
                "mod":self.modEdit.text(),
                "failure_type":self.ftEdit.text(),
                "status":self.statusEdit.text(),
                "sim":self.simEdit.text(),
                "callsign":self.csEdit.text().upper()
            }])],ignore_index=True)
            self.df.to_csv("./src/log.csv",index=False)
            self.allFlights()
        except Exception as e:
            self.exception=QMessageBox.critical(self.addRec,"Error!","Incorrect entry in one or more field(s).")
        finally:
            self.addRec.deleteLater()

    def allFlights(self):
        self.flight.deleteLater()
        try:
            self.flight=Flight(self.data[self.data.callsign==self.df.callsign.loc[self.df.callsign.count()-1]].loc[self.data.dep.count()-1],self.airports,self.aircrafts,parent=self.background)
        except:
            df=pd.DataFrame({"callsign":["SAMPLE"],
                "aircraft":["B738"],
                "dep":["PHOG"],
                "arr":["PHNL"],
                "time":["00:20"],
                "distance":[151]})
            self.flight=Flight(df.iloc[0],self.airports,self.aircrafts,parent=self.background)
        self.flight.show()
        self.searchMod.clear()
        self.searchStatus.clear()
        self.searchCall.clear()
        self.table.deleteLater()
        self.table=Table(self.df,parent=self.tableArea)
        self.table.show()
        
    def byStatus(self):
        try:
            print(self.df[(self.df.status==self.searchStatus.text())].iloc[0])
            # self.flight.deleteLater()
            # self.flight=Flight(self.data[self.data.callsign==self.df.callsign.loc[self.df.callsign.count()-1]].iloc[0],self.airports,self.aircrafts,parent=self.background)
            # self.flight.show()
            self.table.deleteLater()
            self.table=Table(self.df[(self.df.status==self.searchStatus.text())],parent=self.tableArea)
            self.table.show()

        except Exception as e:
            print(e)

        finally:
            self.searchCall.clear()
            self.searchMod.clear()


    def searchCallsign(self):
        try:
            searchCall = self.searchCall.text().upper()
            print(self.df[self.df.callsign==searchCall].iloc[0])
            self.flight.deleteLater()
            self.flight=Flight(self.df[self.df.callsign==searchCall].iloc[0],self.airports,self.aircrafts,parent=self.background)
            self.flight.show()
            self.table.deleteLater()
            self.table=Table(self.df[self.df.callsign==searchCall],parent=self.tableArea)
            self.table.show()

        except Exception as e:
            print(e)
        
        finally:
            self.searchMod.clear()
            self.searchStatus.clear()

    def byMod(self):
        try:
            print(self.df[self.df["mod"]==self.searchMod.text()].iloc[0])
            # self.flight.deleteLater()
            # self.flight=Flight(self.df[self.df["mod"]==self.searchMod.text()].iloc[0],self.airports,self.aircrafts,parent=self.background)
            # self.flight.show()
            self.table.deleteLater()
            self.table=Table(self.df[self.df["mod"]==self.searchMod.text()],parent=self.tableArea)
            self.table.show()

        except Exception as e:
            print(e)
        
        finally:
            self.searchStatus.clear()
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
        self.setSelectionMode(QAbstractItemView.NoSelection)
        
        textStyle='''background:rgba(255, 255, 255, 0);font-size:15px;font-weight:400;color:#515151;border-right:1px solid #515151;border-left:1px solid #515151;border-radius:0px;'''
        for i in range(self.df.callsign.count()-1,-1,-1):
            print(self.df["mod"])
            self.insertRow(self.rowCount())
            self.date=QLabel(text=self.df.date.iloc[i])
            self.date.setFixedSize(147,50)
            self.date.setStyleSheet("background:rgba(255, 255, 255, 0);font-size:15px;font-weight:400;color:#515151;border-right:1px solid #515151;border-radius:0px;")
            self.date.setAlignment(QtCore.Qt.AlignCenter)
            self.setCellWidget(self.rowCount()-1,0,(self.date))

            self.mod=QLabel(text=self.df["mod"].iloc[i])
            self.mod.setFixedSize(147,50)
            self.mod.setStyleSheet(textStyle)
            self.mod.setAlignment(QtCore.Qt.AlignCenter)
            self.setCellWidget(self.rowCount()-1,1,(self.mod))

            self.ft=QLabel(text=self.df.failure_type.iloc[i])
            self.ft.setFixedSize(147,50)
            self.ft.setStyleSheet(textStyle)
            self.ft.setAlignment(QtCore.Qt.AlignCenter)
            self.setCellWidget(self.rowCount()-1,2,self.ft)
            self.ft.setWordWrap(True)

            self.status=QLabel(text=self.df.status.iloc[i])
            self.status.setFixedSize(147,50)
            self.status.setStyleSheet(textStyle)
            self.status.setAlignment(QtCore.Qt.AlignCenter)
            self.setCellWidget(self.rowCount()-1,3,self.status)

            self.sim=QLabel(text=self.df.sim.iloc[i])
            self.sim.setFixedSize(147,50)
            self.sim.setStyleSheet(textStyle)
            self.sim.setAlignment(QtCore.Qt.AlignCenter)
            self.setCellWidget(self.rowCount()-1,4,self.sim)

            self.cs=QLabel(text=str(self.df.callsign.iloc[i]))
            self.cs.setFixedSize(147,50)
            self.cs.setStyleSheet("background:rgba(255, 255, 255, 0);font-size:15px;font-weight:400;color:#515151;border-left:1px solid #515151;border-radius:0px;")
            self.cs.setAlignment(QtCore.Qt.AlignCenter)
            self.setCellWidget(self.rowCount()-1,5,self.cs)
        
        for i in range(self.rowCount()):
            self.setRowHeight(i,50)

if __name__=="__main__":
    df=pd.read_csv("./src/log.csv")
    app = QApplication([])
    window = logBook(parent=None)
    window.show()
    appexe=app.exec()
    sys.exit(appexe)
