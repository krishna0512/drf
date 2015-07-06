import sys
import os.path
import time
import requests
import json
from chat import *
from StringIO import StringIO
from PyQt4 import QtGui, QtCore, uic

form_class = uic.loadUiType("login.ui")[0]
form2_class = uic.loadUiType("register.ui")[0]
form3_class = uic.loadUiType("dialogBox.ui")[0]


class Dialog(QtGui.QDialog,form3_class):
    """A simple Media Player using VLC and Qt
    """
    def __init__(self, message='', master=None):
        QtGui.QMainWindow.__init__(self, master)
        self.setupUi(self)
        self.setWindowTitle("DialogBox")
        self.message = message
        self.setLabel()

    def setMessage(self,msg):
        self.message=msg
        self.setLabel()

    def setLabel(self):
        self.displayText.setText(str(self.message))


class Register(QtGui.QDialog,form2_class):
    """A simple Media Player using VLC and Qt
    """
    def __init__(self, master=None):
        QtGui.QMainWindow.__init__(self, master)
        self.setupUi(self)
        self.setWindowTitle("Register Window")
        self.okButton.clicked.connect(self.register)
        self.cancelButton.clicked.connect(self.close)

    def register(self):
        for i in ('username','password','email','fname','lname'):
            exec ("%sValue = str(self.%s.toPlainText()).strip()" % (i,i))
        isTA = self.checkBox.isChecked()
        if all(a != '' for a in (usernameValue, passwordValue, emailValue, fnameValue, lnameValue)):
            payload = {
                    'username'  : str (usernameValue),
                    'pass'      : str (passwordValue),
                    'email'     : str (emailValue),
                    'lname'     : str (lnameValue),
                    'fname'     : str (fnameValue),
                    'ista'      : str (isTA)
                    }
            url = 'http://localhost:8000/polls/Register/'
            r=requests.get(url,params=payload)
            if int(r.status_code) == 500:
                self.dlg = Dialog('Username already aquired...')
                self.dlg.show()
            else:
                self.dlg = Dialog(r.text+' successfully registered', self)
                self.dlg.show()
                self.hide()
        else: Dialog('Field Missing!', self).show()

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore() 

    
class Login(QtGui.QMainWindow,form_class):
    """A simple Media Player using VLC and Qt
    """
    def __init__(self, master=None):
        QtGui.QMainWindow.__init__(self, master)
        self.setupUi(self)
        self.setWindowTitle("Login Window")
        self.registerButton.clicked.connect(self.openRegisteration)
        self.loginButton.clicked.connect(self.login)
        self.cancelButton.clicked.connect(self.closeWindow)
        self.sessionid = ''
        self.dlgw=[]

    def login(self):
        usernameValue =str(self.username.toPlainText()).strip()
        passwordValue =str(self.password.toPlainText()).strip()
        if usernameValue == '' or passwordValue == '':
            self.dlg=Dialog('Field Missing!')
            self.dlg.show()
        else:
            payload = {
                    'username' : str (usernameValue),
                    'pass'     : str (passwordValue)
                    }
            url = 'http://localhost:8000/polls/Login/'
            r = requests.get(url,params=payload)
            print r.text
            if r.text == '':
                self.dlg = Dialog("username or password incorrect")
                self.dlg.show()
            else:
                # Login Successfull
                self.sessionid = r.cookies['sessionid']
                # self is passed in the chat to gain the access to
                # self.sessionid variable..
                self.chat = Chat(self)
                self.chat.show()
                self.hide()

    def openRegisteration(self):
        self.reg = Register()
        self.reg.show()

    def closeWindow(self):
        QtCore.QCoreApplication.instance().quit()

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()       


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec_())

