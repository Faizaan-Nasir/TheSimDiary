import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer
import mysql.connector as sql
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import haversine as hs   
from haversine import Unit

# DEPRECATED
 
loc1=(19.0760, 72.8777)
loc2=(18.5204, 73.8567)
 
result=hs.haversine(loc1,loc2,unit=Unit.KILOMETERS)
print("The distance calculated is:",result)

app = QApplication([])

window=QWidget()
window.setWindowTitle("PilotDiary")
window.setWindowIcon(QtGui.QIcon('./src/icon.ico'))
window.setFixedWidth(1400)
window.setFixedHeight(750)
window.setStyleSheet('background:url("./src/background.jpg") center') 

check=False

def loginc():
    global cur
    global con
    try:
        pwd=pwde.text()
        db=dbe.text()
        try:
            con=sql.connect(host='localhost',user='root',password=pwd,database=db)
        except:
            con=sql.connect(host='localhost',user='root',password=pwd)
            cur=con.cursor()
            cur.execute('create database '+db)
            con.close()
            con=sql.connect(host='localhost',user='root',password=pwd,database=db)

        passwordf=open('pwd.txt','x')
        passwordf.close()
        dbf=open('db.txt','x')
        dbf.close()
        password=open('pwd.txt','w')
        password.write(pwd)
        password.close()
        datab=open('db.txt','w')
        datab.write(db)
        datab.close()
        login.destroy()
        window.show()
        cur=con.cursor()
        newdata()
        window.show()
    except Exception as e:
        print(e)
        error=QLabel('Incorrect Credentials!',parent=login)
        error.setStyleSheet('color:#F04E4E;font-size:25px;font-weight:500')
        error.move(20,5)
        error.show()

try:
    pwd=open('pwd.txt','r').read()
    db=open('db.txt','r').read()
    con=sql.connect(host='localhost',user='root',password=pwd,database=db)
    cur=con.cursor()
    df=pd.read_sql("select * from flights;",con)
    df.to_csv("./src/data.csv",index=False)
except:
    check=True
    login=QWidget()
    login.setWindowTitle("Login")
    login.setWindowIcon(QtGui.QIcon('./src/icon.ico'))
    login.setFixedHeight(340)
    login.setFixedWidth(800)
    
    title=QLabel('LOGIN',parent=login)
    title.setFixedWidth(800)
    title.setAlignment(QtCore.Qt.AlignCenter)
    title.setStyleSheet('font-size:45px;font-weight:900')
    title.move(0,10)
    title.show()
    
    pwdl=QLabel('Password: ',parent=login)
    pwdl.setStyleSheet('font-size:35px;font-weight:600')
    pwdl.move(30,90)
    pwdl.show()
    
    pwde=QLineEdit(parent=login)
    pwde.setFixedWidth(350)
    pwde.setPlaceholderText('enter password here')
    pwde.setStyleSheet('font-size:25px;border:none;background:white;border-radius:10px;padding:10px')
    pwde.move(250,87)
    
    dbl=QLabel('Database: ',parent=login)
    dbl.setStyleSheet('font-size:35px;font-weight:600')
    dbl.move(30,170)
    dbl.show()
    
    dbe=QLineEdit('pilotdiary',parent=login)
    dbe.setFixedWidth(350)
    dbe.setPlaceholderText('enter db name here')
    dbe.setStyleSheet('font-size:25px;border:none;background:white;border-radius:10px;padding:10px')
    dbe.move(250,167)
    
    submit=QPushButton('Submit',parent=login)
    submit.setFixedWidth(300)
    submit.setStyleSheet('background:#F04E4E;border-radius:10px;font-size:25px;padding:10px;color:white;font-weight:500')
    submit.move(250,250)
    submit.clicked.connect(loginc)
    submit.show()
    
    login.show()

# win=Stats()
# win.show() 

heading=QLabel('The Pilot Diary',parent=window)
heading.setFixedWidth(1350)
heading.move(0,40)
heading.setAlignment(QtCore.Qt.AlignCenter)
heading.setStyleSheet("background:rgba(255, 255, 255, 0.725);font-size:45px;font-weight:800;padding:8px;margin-left:50px;border-radius:10px")
heading.show()

infoareabar=QWidget(parent=window)
infoareabar.setFixedWidth(1300)
infoareabar.move(50,125)
infoareabar.setFixedHeight(50)
infoareabar.setStyleSheet('background:rgba(255, 255, 255, 0.725);border-radius:10px')
infoareabar.show()

tdistance=QLabel('Distance Flown: ')
thours=QLabel('Hours: ')
flights=QLabel('Flights: ')
upname=QLabel('Pilot Name: ')
def repeat():
    global tdistance
    global thours
    global nofl
    global uairc
    global uairline
    global uhub
    global upname
    global pname
    global flights
    try:
        cur.execute('select * from pInfo')
        data=cur.fetchall()
        upname=data[-1][0]
        uairc=data[-1][1]
        uairline=data[-1][2]
        uhub=data[-1][3]
    except:
        upname=''
        uairc=''
        uairline=''
        uhub=''
        df=''
        fh=''
    try:
        cur.execute('select * from flights;')
        newdata=cur.fetchall()
        nofl=len(newdata)
        tot=0
        hours=0
        mins=0
        for i in newdata:
            tot+=int(i[-1])
            hours+=int(i[-2][0:2])
            mins+=int(i[-2][3:])
        if mins>=60:
            hours+=mins//60
            mins=mins%60
        df=str(tot)
        fh=str(hours)+' hrs '+str(mins)+' mins'
    except:
        df=''
        fh=''
        nofl=0
    finally:
        tdistance.deleteLater()
        thours.deleteLater()
        tdistance=QLabel('Distance Flown: '+df+' km',parent=window)
        tdistance.move(0,130)
        tdistance.setAlignment(QtCore.Qt.AlignCenter)
        tdistance.setFixedWidth(1400)
        tdistance.setStyleSheet("border-radius:10px;background:transparent;font-size:30px;font-weight:600;")
        tdistance.show()
        thours=QLabel('Hours: '+fh,parent=window)
        thours.move(0,130)
        thours.setStyleSheet('font-weight:600;background:transparent;font-size:30px;margin-left:75px;')
        thours.show()
        flights.deleteLater()
        flights=QLabel('Total Flights: '+str(nofl),parent=window)
        flights.move(0,130)
        flights.setFixedWidth(1400)
        flights.setAlignment(QtCore.Qt.AlignRight)
        flights.setStyleSheet("background:transparent;font-size:30px;font-weight:600;margin-right:75px;")
        flights.show()
    QTimer.singleShot(1000,repeat)
repeat()


def editinfo():
    try:
        cur.execute('select * from pInfo')
        cur.fetchall()
    except:
        cur.execute('create table pInfo (name varchar(60),airc varchar(30),airline varchar(30),hub varchar(20));')
        con.commit()
    infotitle.show()
    infowin.show()

# declaration of info window to be shown later
def submitinfo():
    try:
        cur.execute('insert into pInfo values("{}","{}","{}","{}")'.format(epinfoe.text(),airce.text(),airle.text(),hube.text()))
        con.commit()
    except Exception as e:
        mbox=QMessageBox.critical(newlog,"Error!","You have entered incorrect format")
    infowin.destroy()
infowin=QWidget()
infowin.setWindowTitle('Edit Info')
infowin.setWindowIcon(QtGui.QIcon('./src/icon.ico'))
infowin.setFixedHeight(500)
infowin.setFixedWidth(1000)
infotitle=QLabel('Edit Info',parent=infowin)
infotitle.setStyleSheet('font-size:45px;font-weight:900')
infotitle.setFixedWidth(1000)
infotitle.setAlignment(QtCore.Qt.AlignCenter)
infotitle.move(0,10)
epinfo=QLabel('Pilot Name:',parent=infowin)
epinfo.setStyleSheet('font-size:25px;font-weight:600;background:transparent;')
epinfo.move(50,95)
epinfoe=QLineEdit(parent=infowin)
epinfoe.setStyleSheet('font-size:25px;border:none;background:white;border-radius:10px;padding:10px')
epinfoe.setFixedWidth(350)
epinfoe.move(325,85)
epinfoe.setPlaceholderText('enter pilot name')
airc=QLabel('Aircraft(s) Flown:',parent=infowin)
airc.setStyleSheet('font-size:25px;font-weight:600;background:transparent;')
airc.move(50,175)
airce=QLineEdit(parent=infowin)
airce.setStyleSheet('font-size:25px;border:none;background:white;border-radius:10px;padding:10px')
airce.setFixedWidth(350)
airce.move(325,165)
airce.setPlaceholderText('enter aircraft(s) icao')
airl=QLabel('Current Airline:',parent=infowin)
airl.setStyleSheet('font-size:25px;font-weight:600;background:transparent;')
airl.move(50,255)
airle=QLineEdit(parent=infowin)
airle.setStyleSheet('font-size:25px;border:none;background:white;border-radius:10px;padding:10px')
airle.setFixedWidth(350)
airle.move(325,245)
airle.setPlaceholderText('enter airline name (icao)')
hub=QLabel('Hub City:',parent=infowin)
hub.setStyleSheet('font-size:25px;font-weight:600;background:transparent;')
hub.move(50,335)
hube=QLineEdit(parent=infowin)
hube.setStyleSheet('font-size:25px;border:none;background:white;border-radius:10px;padding:10px')
hube.setFixedWidth(350)
hube.move(325,325)
hube.setPlaceholderText('enter city hub')
subinfo=QPushButton('Submit',parent=infowin)
subinfo.setStyleSheet('background:#F04E4E;border-radius:10px;font-size:25px;padding:10px;color:white;font-weight:500')
subinfo.setFixedWidth(300)
subinfo.move(350,410)
subinfo.clicked.connect(submitinfo)

infoarea=QWidget(parent=window)
infoarea.move(0,190)
infoarea.setFixedHeight(520)
infoarea.setFixedWidth(500)
infoarea.setStyleSheet('border-radius:10px;background:rgba(255, 255, 255, 0.725);margin-left:50px;')
layout=QVBoxLayout()
titleinfo=QLabel('General Info')
titleinfo.setFixedWidth(478)
titleinfo.setFixedHeight(50)
titleinfo.setStyleSheet('font-size:30px;font-weight:600;background:transparent;')
titleinfo.setAlignment(QtCore.Qt.AlignCenter)
layout.addWidget(titleinfo)
infoedit=QPushButton('Edit Info')
infoedit.setStyleSheet('background:#F04E4E;border-radius:10px;font-size:20px;padding:10px;color:white;font-weight:700')
layout.addWidget(infoedit)
infoedit.clicked.connect(editinfo)
pinfoname=QLabel('Pilot Name: '+upname)
pinfoname.setStyleSheet('font-size:25px;font-weight:600;background:transparent;')
layout.addWidget(pinfoname)
pinfotype=QLabel('Aircraft Type(s): '+uairc)
pinfotype.setStyleSheet('font-size:25px;font-weight:600;background:transparent;')
layout.addWidget(pinfotype)
pinfoair=QLabel('Current Airline: '+uairline)
pinfoair.setStyleSheet('font-size:25px;font-weight:600;background:transparent;')
layout.addWidget(pinfoair)
pinfohub=QLabel('Current Hub: '+uhub)
pinfohub.setStyleSheet('font-size:25px;font-weight:600;background:transparent;')
layout.addWidget(pinfohub)
tinfo=QLabel('UTC Time: '+str(datetime.utcnow().hour)+' hrs '+str(datetime.utcnow().minute)+' mins')
tinfo.setStyleSheet('font-size:25px;font-weight:600;background:transparent;')
layout.addWidget(tinfo)
def updateinfo():
    global pinfoname
    global pinfotype
    global pinfoair
    global pinfohub
    global tinfo
    pinfoname.deleteLater()
    pinfoname=QLabel('Pilot Name: '+upname)
    pinfoname.setStyleSheet('font-size:25px;font-weight:600;background:transparent;')
    layout.addWidget(pinfoname)
    pinfotype.deleteLater()
    pinfotype=QLabel('Aircraft Type(s): '+uairc)
    pinfotype.setStyleSheet('font-size:25px;font-weight:600;background:transparent;')
    layout.addWidget(pinfotype)
    pinfoair.deleteLater()
    pinfoair=QLabel('Current Airline: '+uairline)
    pinfoair.setStyleSheet('font-size:25px;font-weight:600;background:transparent;')
    layout.addWidget(pinfoair)
    pinfohub.deleteLater()
    pinfohub=QLabel('Current Hub: '+uhub)
    pinfohub.setStyleSheet('font-size:25px;font-weight:600;background:transparent;')
    layout.addWidget(pinfohub)
    tinfo.deleteLater()
    tinfo=QLabel('UTC Time: '+str(datetime.utcnow().hour)+' hrs '+str(datetime.utcnow().minute)+' mins')
    tinfo.setStyleSheet('font-size:25px;font-weight:600;background:transparent;')
    layout.addWidget(tinfo)
    infoarea.setLayout(layout)
    QTimer.singleShot(1000,updateinfo)
updateinfo()
infoarea.setLayout(layout)

tablearea=QWidget(parent=window)
tablearea.move(465,190)
tablearea.setStyleSheet('border-radius:10px;background:rgba(255, 255, 255, 0.725);margin-left:50px;')
tablearea.setFixedHeight(520)
tablearea.setFixedWidth(885)
tablearea.show()
grid=QGridLayout()
cs=QLabel("<div style='font-size:22px;background:transparent;font-weight:700'>Callsign</div>")
cs.setStyleSheet('background:transparent;')
airc=QLabel("<div style='font-size:22px;background:transparent;font-weight:700'>Aircraft</div>")
airc.setStyleSheet('background:transparent;')
dep=QLabel("<div style='font-size:22px;font-weight:700'>Dep.</div>")
dep.setStyleSheet('background:transparent;')
arr=QLabel("<div style='font-size:22px;font-weight:700'>Arr.</div>")
arr.setStyleSheet('background:transparent;')
time=QLabel("<div style='font-size:22px;background:transparent;font-weight:700'>Air Time</div>")
time.setStyleSheet('background:transparent;')
dst=QLabel("<div style='font-size:22px;background:transparent;font-weight:800'>Dist. (km)</div>")
dst.setStyleSheet('background:transparent;')
grid.addWidget(cs,1,1)
grid.addWidget(airc,1,2)
grid.addWidget(dep,1,3)
grid.addWidget(arr,1,4)
grid.addWidget(time,1,5)
grid.addWidget(dst,1,6)

def newdata():
    try:
        cur.execute('select * from flights;')
    except:
        cur.execute('create table flights (callsign varchar (10) , aircraft varchar (4) , dep varchar (20) , arr varchar (20) , time varchar (20) , distance varchar (10));')
        cur.execute('select * from flights;')
    children=[]
    for q in range(6,grid.count()):
        child=grid.itemAt(q).widget()
        if child:
            children.append(child)
    for child in children:
        child.deleteLater()
    a=2
    b=1
    data=cur.fetchall()
    for i in range(-1,-6,-1):
        try:
            m=data[i]
            if a!=6:
                for j in m:
                    temp=QLabel("<div style='font-size:20px;background:transparent;font-weight:500'>"+j+"</div>")
                    temp.setStyleSheet('background:transparent')
                    grid.addWidget(temp,a,b)
                    b+=1
            else:
                raise Exception('move next')
            a+=1
            b=1
        except:
            temp=QLabel("<div style='font-size:20px;background:transparent;font-weight:500'>""</div>")
            temp.setStyleSheet('background:transparent')
            grid.addWidget(temp,a,b)
            if a==6:
                break
            a+=1
def addflight():
    newfl.show()
def subflight():
    df=pd.read_csv("./src/airport-codes.csv")
    coor1=df.coordinates[df.icao_code==depare.text()].iloc[0].split(',')
    coor2=df.coordinates[df.icao_code==arrie.text()].iloc[0].split(',')
    coor1[0]=float(coor1[0])
    coor1[1]=float(coor1[1])
    coor2[0]=float(coor2[0])
    coor2[1]=float(coor2[1])
    result=int(hs.haversine(coor1,coor2,unit=Unit.KILOMETERS))
    try:
        cur.execute('insert into flights values("{}","{}","{}","{}","{}","{}");'.format(callsie.text(),aircue.text(),depare.text(),arrie.text(),airtie.text(),result))
        con.commit()
    except:
        mbox=QMessageBox.critical(newlog,"Error!","You have entered incorrect format")
    newdata()
    newfl.hide()

# creating window to be shown later
newfl=QWidget()
newfl.setWindowIcon(QtGui.QIcon('./src/icon.ico'))
newfl.setFixedHeight(600)
newfl.setFixedWidth(1000)
newfl.setWindowTitle('New Flight')
newflti=QLabel('New Flight',parent=newfl)
newflti.setFixedWidth(1000)
newflti.setAlignment(QtCore.Qt.AlignCenter)
newflti.setStyleSheet('font-size:45px;font-weight:900')
newflti.move(0,10)
callsi=QLabel('Callsign:',parent=newfl)
callsi.setStyleSheet('font-size:25px;font-weight:600;background:transparent;')
callsi.move(50,95)
callsie=QLineEdit(parent=newfl)
callsie.setStyleSheet('font-size:25px;border:none;background:white;border-radius:10px;padding:10px')
callsie.setFixedWidth(350)
callsie.move(325,85)
callsie.setPlaceholderText('enter callsign')
aircu=QLabel('Aircraft Flown:',parent=newfl)
aircu.setStyleSheet('font-size:25px;font-weight:600;background:transparent;')
aircu.move(50,165)
aircue=QLineEdit(parent=newfl)
aircue.setStyleSheet('font-size:25px;border:none;background:white;border-radius:10px;padding:10px')
aircue.setFixedWidth(350)
aircue.move(325,155)
aircue.setPlaceholderText('enter aircraft icao')
depar=QLabel('Departure:',parent=newfl)
depar.setStyleSheet('font-size:25px;font-weight:600;background:transparent;')
depar.move(50,235)
depare=QLineEdit(parent=newfl)
depare.setStyleSheet('font-size:25px;border:none;background:white;border-radius:10px;padding:10px')
depare.setFixedWidth(350)
depare.move(325,225)
depare.setPlaceholderText('enter departure airport (icao)')
arri=QLabel('Arrival:',parent=newfl)
arri.setStyleSheet('font-size:25px;font-weight:600;background:transparent;')
arri.move(50,305)
arrie=QLineEdit(parent=newfl)
arrie.setStyleSheet('font-size:25px;border:none;background:white;border-radius:10px;padding:10px')
arrie.setFixedWidth(350)
arrie.move(325,295)
arrie.setPlaceholderText('enter arrival airport (icao)')
airti=QLabel('Air Time:',parent=newfl)
airti.setStyleSheet('font-size:25px;font-weight:600;background:transparent;')
airti.move(50,375)
airtie=QLineEdit(parent=newfl)
airtie.setStyleSheet('font-size:25px;border:none;background:white;border-radius:10px;padding:10px')
airtie.setFixedWidth(350)
airtie.move(325,365)
airtie.setPlaceholderText('enter time (hh:mm)')
distan=QLabel('Distance:',parent=newfl)
distan.setStyleSheet('font-size:25px;font-weight:600;background:transparent;')
distan.move(50,445)
distane=QLineEdit(parent=newfl)
distane.setStyleSheet('font-size:25px;border:none;background:white;border-radius:10px;padding:10px')
distane.setFixedWidth(350)
distane.move(325,435)
distane.setPlaceholderText('enter distance')
subfli=QPushButton('Submit',parent=newfl)
subfli.setStyleSheet('background:#F04E4E;border-radius:10px;font-size:25px;padding:10px;color:white;font-weight:500')
subfli.setFixedWidth(300)
subfli.move(350,510)
subfli.clicked.connect(subflight)

addfl=QPushButton('Add Flight',parent=window)
addfl.setStyleSheet('background:#F04E4E;border-radius:10px;font-size:20px;padding:10px;color:white;font-weight:700')
addfl.setFixedWidth(300)
addfl.move(622,635)
addfl.show()
addfl.clicked.connect(addflight)

book=QWidget()
book.setFixedHeight(750)
book.setFixedWidth(1400)
book.setWindowTitle("Aircrafts Logbook")
book.setWindowIcon(QtGui.QIcon('./src/icon.ico'))
book.setStyleSheet('background:url("./src/background.jpeg") center')
backdrop=QWidget(parent=book)
backdrop.setStyleSheet('border-radius:10px;background:rgba(255, 255, 255, 0.725)')
backdrop.setFixedHeight(650)
backdrop.setFixedWidth(1300)
backdrop.move(50,50)
titlebook=QLabel('Log Book',parent=backdrop)
titlebook.setAlignment(QtCore.Qt.AlignCenter)
titlebook.setFixedWidth(1300)
titlebook.setStyleSheet("background:rgba(255, 255, 255, 0.0);font-size:45px;font-weight:800;padding:8px;border-radius:10px")
tablearealog=QScrollArea(parent=backdrop)
tablearealog.move(45,80)
tablearealog.setStyleSheet('border-radius:10px;background:transparent; border: 5px solid white')
tablearealog.setFixedHeight(480)
tablearealog.setFixedWidth(1200)
tablearealog.setWidgetResizable(True)
tablearealog.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
tablearealog.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
logtable=QGridLayout(book)
title1=QLabel("<div style='font-size:22px;background:transparent;font-weight:800'>Date</div>")
title1.setStyleSheet("background:transparent;")
title1.setFixedWidth(225)
title1.setFixedHeight(50)
title1.setAlignment(QtCore.Qt.AlignCenter)
title2=QLabel("<div style='font-size:22px;background:transparent;font-weight:800'>Callsign</div>")
title2.setStyleSheet("background:transparent;")
title2.setFixedWidth(225)
title2.setFixedHeight(50)
title2.setAlignment(QtCore.Qt.AlignCenter)
title3=QLabel("<div style='font-size:22px;background:transparent;font-weight:800'>Registration</div>")
title3.setStyleSheet("background:transparent;")
title3.setFixedWidth(225)
title3.setFixedHeight(50)
title3.setAlignment(QtCore.Qt.AlignCenter)
title4=QLabel("<div style='font-size:22px;background:transparent;font-weight:800'>Comments</div>")
title4.setStyleSheet("background:transparent;")
title4.setFixedWidth(490)
title4.setFixedHeight(50)
title4.setAlignment(QtCore.Qt.AlignCenter)
logtable.addWidget(title1,0,0)
logtable.addWidget(title2,0,1)
logtable.addWidget(title3,0,2)
logtable.addWidget(title4,0,3)

tablearealog.setLayout(logtable)
def logbook():
    try:
        cur.execute("select * from log")
        row=1
        data=cur.fetchall()
        for i in range (len(data)-1,-1,-1):
            a="<div style='font-size:22px;background:transparent;font-weight:300'>"+str(data[i][0])+"</div>"
            col1=QLabel(a)
            col1.setStyleSheet("background:transparent;")
            col1.setAlignment(QtCore.Qt.AlignCenter)
            col1.setFixedWidth(225)
            col1.setFixedHeight(50)
            b="<div style='font-size:22px;background:transparent;font-weight:300'>"+str(data[i][1])+"</div>"
            col2=QLabel(b)
            col2.setStyleSheet("background:transparent;")
            col2.setAlignment(QtCore.Qt.AlignCenter)
            col2.setFixedWidth(225)
            col2.setFixedHeight(50)
            c="<div style='font-size:22px;background:transparent;font-weight:300'>"+str(data[i][2])+"</div>"
            col3=QLabel(c)
            col3.setStyleSheet("background:transparent;")
            col3.setAlignment(QtCore.Qt.AlignCenter)
            col3.setFixedWidth(225)
            col3.setFixedHeight(50)
            d="<div style='font-size:22px;background:transparent;font-weight:300'>"+str(data[i][3])+"</div>"
            col4=QLabel(d)
            col4.setStyleSheet("background:transparent;")
            col4.setAlignment(QtCore.Qt.AlignCenter)
            col4.setFixedWidth(490)
            col4.setFixedHeight(50)
            logtable.addWidget(col1,row,0)
            logtable.addWidget(col2,row,1)
            logtable.addWidget(col3,row,2)
            logtable.addWidget(col4,row,3)
            row+=1
        else:
            if row<8:
                for i in range(8-row+1):
                    col1=QLabel("<div style='font-size:22px;background:transparent;font-weight:300'></div>")
                    col1.setStyleSheet("background:transparent;")
                    col1.setFixedWidth(225)
                    col1.setFixedHeight(50)
                    col2=QLabel("<div style='font-size:22px;background:transparent;font-weight:300'></div>")
                    col2.setStyleSheet("background:transparent;")
                    col2.setFixedWidth(225)
                    col2.setFixedHeight(50)
                    col3=QLabel("<div style='font-size:22px;background:transparent;font-weight:300'></div>")
                    col3.setStyleSheet("background:transparent;")
                    col3.setFixedWidth(225)
                    col3.setFixedHeight(50)
                    col4=QLabel("<div style='font-size:22px;background:transparent;font-weight:300'></div>")
                    col4.setStyleSheet("background:transparent;")
                    col4.setFixedWidth(490)
                    col4.setFixedHeight(50)
                    logtable.addWidget(col1,i+1,0)
                    logtable.addWidget(col2,i+1,1)
                    logtable.addWidget(col3,i+1,2)
                    logtable.addWidget(col4,i+1,3)
    except Exception as e:
        print(e)
        cur.execute("create table log (date varchar(8),fno varchar(10),registration varchar(8),comment varchar(400))")
        con.commit()
        for i in range(8):
            col1=QLabel("<div style='font-size:22px;background:transparent;font-weight:300'></div>")
            col1.setStyleSheet("background:transparent;")
            col1.setFixedWidth(225)
            col1.setFixedHeight(50)
            col2=QLabel("<div style='font-size:22px;background:transparent;font-weight:300'></div>")
            col2.setStyleSheet("background:transparent;")
            col2.setFixedWidth(225)
            col2.setFixedHeight(50)
            col3=QLabel("<div style='font-size:22px;background:transparent;font-weight:300'></div>")
            col3.setStyleSheet("background:transparent;")
            col3.setFixedWidth(225)
            col3.setFixedHeight(50)
            col4=QLabel("<div style='font-size:22px;background:transparent;font-weight:300'></div>")
            col4.setStyleSheet("background:transparent;")
            col4.setFixedWidth(490)
            col4.setFixedHeight(50)
            logtable.addWidget(col1,i+1,0)
            logtable.addWidget(col2,i+1,1)
            logtable.addWidget(col3,i+1,2)
            logtable.addWidget(col4,i+1,3)
    book.show()
    window.hide()
    new=QWidget()
    new.setStyleSheet('border:0')
    new.setLayout(logtable)
    tablearealog.setWidget(new)
    tablearealog.show()
    
    def submlog():
        try:
            cur.execute('insert into log values("{}","{}","{}","{}");'.format(datee.text(),ace.text(),rege.text(),come.text()))
            con.commit()
        except:
            mbox=QMessageBox.critical(newlog,"Error!","You have entered incorrect format")
        newlog.hide()
    newlog=QWidget()
    newlog.setWindowIcon(QtGui.QIcon('./src/icon.ico'))
    newlog.setFixedHeight(450)
    newlog.setFixedWidth(1000)
    newlog.setWindowTitle('New Log')
    newlogti=QLabel('New Log',parent=newlog)
    newlogti.setFixedWidth(1000)
    newlogti.setAlignment(QtCore.Qt.AlignCenter)
    newlogti.setStyleSheet('font-size:45px;font-weight:900')
    newlogti.move(0,10)
    date=QLabel('Date:',parent=newlog)
    date.setStyleSheet('font-size:25px;font-weight:600;background:transparent;')
    date.move(50,95)
    datee=QLineEdit(parent=newlog)
    datee.setStyleSheet('font-size:25px;border:none;background:white;border-radius:10px;padding:10px')
    datee.setFixedWidth(350)
    datee.move(325,85)
    datee.setPlaceholderText('enter date')
    ac=QLabel('Callsign:',parent=newlog)
    ac.setStyleSheet('font-size:25px;font-weight:600;background:transparent;')
    ac.move(50,165)
    ace=QLineEdit(parent=newlog)
    ace.setStyleSheet('font-size:25px;border:none;background:white;border-radius:10px;padding:10px')
    ace.setFixedWidth(350)
    ace.move(325,155)
    ace.setPlaceholderText('enter callsign')
    reg=QLabel('Registration:',parent=newlog)
    reg.setStyleSheet('font-size:25px;font-weight:600;background:transparent;')
    reg.move(50,235)
    rege=QLineEdit(parent=newlog)
    rege.setStyleSheet('font-size:25px;border:none;background:white;border-radius:10px;padding:10px')
    rege.setFixedWidth(350)
    rege.move(325,225)
    rege.setPlaceholderText('enter registration')
    com=QLabel('Comments:',parent=newlog)
    com.setStyleSheet('font-size:25px;font-weight:600;background:transparent;')
    com.move(50,305)
    come=QLineEdit(parent=newlog)
    come.setStyleSheet('font-size:25px;border:none;background:white;border-radius:10px;padding:10px')
    come.setFixedWidth(350)
    come.move(325,295)
    come.setPlaceholderText('enter comments')
    sublog=QPushButton('Submit',parent=newlog)
    sublog.setStyleSheet('background:#F04E4E;border-radius:10px;font-size:25px;padding:10px;color:white;font-weight:500')
    sublog.setFixedWidth(300)
    sublog.move(350,370)
    sublog.clicked.connect(submlog)
    def newrec():
        newlog.show()
    addNew=QPushButton('New Record',parent=book)
    addNew.setStyleSheet('background:#F04E4E;border-radius:10px;font-size:20px;padding:10px;color:white;font-weight:700')
    addNew.setFixedWidth(300)
    addNew.move(710,635)
    addNew.show()
    addNew.clicked.connect(newrec)
    def back():
        book.hide()
        window.show()
    backout=QPushButton('Go Back',parent=book)
    backout.setStyleSheet('background:#F04E4E;border-radius:10px;font-size:20px;padding:10px;color:white;font-weight:700')
    backout.setFixedWidth(300)
    backout.move(390,635)
    backout.show()
    backout.clicked.connect(back)
log=QPushButton('Log Book',parent=window)
log.setStyleSheet('background:#F04E4E;border-radius:10px;font-size:20px;padding:10px;color:white;font-weight:700')
log.setFixedWidth(300)
log.move(942,635)
log.show()
log.clicked.connect(logbook)

tablearea.setLayout(grid)


if check:
    pass
else:
    window.show()
    newdata()

appexe=app.exec()
sys.exit(appexe)