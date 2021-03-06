import sys
import os.path
import time
import requests
import json
from   dialog     import Dialog
from   chat       import *
from   StringIO   import StringIO
from   PyQt4      import QtGui, QtCore, uic
from   chat         import *
import snc_server
import snc_client 
from header import *

class TaView(QtGui.QWidget):
    '''
        A simple class to present question to check presence
    '''
    def __init__(self,master=None):
        QtGui.QMainWindow.__init__(self, master)
        self.setWindowTitle('LoggedinUsers')
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.updateUI)
        self.timer.start()
        self.setGeometry(0,0,200,10)
        self.setMinimumSize(200,300)

        self.payload = {}
        self.payload['isPaused'] = False
        self.payload['synVideo'] = False
        self.payload['currentPosition'] = 0
        self.payload['isStopped'] = False
        self.sessionid = ''
        self.cookies = ''
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def postSessionid (self, sid):
        self.sessionid = sid
        self.cookies = {'sessionid':self.sessionid}

        self.snc = snc_server.Player(self, self.sessionid)
        self.snc.show()
        self.updateUI()

    def updateUI(self):
        if self.snc == None: print "snc_server is None.."
        url = URL + 'GetAllUsers/'
        r           =   requests.get(url,cookies=self.cookies)
        users       =   json.loads(r.text)
        students    =   users['student']
        ta          =   users['ta']
        url = URL + 'GetLoggedinUsers/'
        r           =   requests.get(url,cookies=self.cookies)
        linUsers    =   json.loads(r.text)
        linStudents =   linUsers['student']
        linTA       =   linUsers['ta']
        if self.layout():
            QtGui.QWidget().setLayout(self.layout())    
        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(10)

        self.lbl  = []      # name of the TAs
        self.lbbl = []      # name of the Students
        self.cir  = []      # the storage of the circles
        self.ques = []      # gives weather question is true or false by the user.
        self.header1    = QtGui.QLabel('TAs:', self)
        self.header2    = QtGui.QLabel('Students:', self)

        # getting the correct and incorrect users for the lastest question.
        url = URL + 'GetStatusOfQuestion/'
        r = requests.get(url)
        t = str(r.text)
        # List of the the users that gave the correct answer to latest question.
        cor = filter(None, t.split(';')[0].split(','))
        # List of the users that gave incorrect answers to the latest question.
        incor = filter(None, t.split(';')[1].split(','))
        print cor
        print incor


        self.grid.addWidget(self.header1, 1, 0, 1, 5)
        j = 0
        uin = 0
        for i in ta:
            self.lbl.append(QtGui.QLabel(str(i), self))
            self.grid.addWidget(self.lbl[j], 2+j, 1, 1, 4)
            if i in linTA:
                self.cir.append(QtGui.QLabel(u'\u25cf',self))
                self.cir[uin].setStyleSheet("QLabel {color:#30ca30}")
                self.grid.addWidget(self.cir[uin], 2+j, 0)
                uin += 1
            j += 1

        self.grid.addWidget(self.header2, 3+j, 0, 1, 5)
        k = 0
        uid2 = 0
        for i in students:
            self.lbbl.append(QtGui.QLabel(str(i),self))
            self.grid.addWidget(self.lbbl[k], 4+j+k, 1, 1, 4)
            if i in linStudents:
                self.cir.append(QtGui.QLabel(u'\u25cf',self))
                self.cir[uin].setStyleSheet("QLabel {color:#30ca30}")
                self.grid.addWidget(self.cir[uin], 4+j+k, 0)
                print str(i)
                if str(i) in cor:
                    print "in correct"
                    self.ques.append (QtGui.QLabel(u"\u2714",self))
                elif str(i) in incor:
                    print "in incorrect"
                    self.ques.append (QtGui.QLabel(u"\u274C",self))
                else:
                    self.ques.append (QtGui.QLabel('-',self))
                self.grid.addWidget (self.ques[uid2], 4+j+k, 5)
                uid2 += 1
                uin += 1
            k += 1
        self.setLayout(self.grid) 
        self.scroll = QtGui.QScrollArea()
        self.scroll.setWidgetResizable(True)
        w2 = QtGui.QWidget(self)
        w2.setLayout(self.grid)
        self.scroll.setWidget(w2)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.scroll)
        self.setLayout(layout)
              

    def submit(self):
        submitedAns=[]
        for i in xrange(len(self.cb)):
            if self.cb[i].isChecked():
                submitedAns.append(True)
            else:
                submitedAns.append(False)
        url = URL + 'SubAns/'
        payload = {'options':submitedAns}
        r=requests.get(url,params=payload,cookies=self.cookies)
        self.hide()

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            self.payload['synVideo'] = False
            data = json.dumps(self.payload)
            data = {'data':data}
            url = URL + 'PostCurSet/'
            r=requests.get(url,params = data,cookies=self.cookies)
            r=requests.get(URL + 'Logout/', cookies=self.cookies)
            print 'about to exit'
            event.accept()
        else:
            event.ignore() 
      


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    view = TaView()
    view.show()
    sys.exit(app.exec_())

