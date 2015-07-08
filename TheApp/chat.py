import sys
import os.path
import requests
import json
from StringIO import StringIO
from PyQt4 import QtGui, QtCore, uic

form_class = uic.loadUiType("chat.ui")[0]
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


class Chat(QtGui.QMainWindow,form_class):
    """
        A simple chat box
    """
    def __init__(self, master=None):
        QtGui.QMainWindow.__init__(self, master)
        self.setupUi(self)
        self.setWindowTitle("Chat Window")

        self.submitButton.clicked.connect(self.submit)
        self.resetButton.clicked.connect(self.reset)
        self.menuTimed.triggered.connect(self.changeViewToTimed)
        self.menuThreaded.triggered.connect(self.changeViewToThreaded)
        self.currentView = 'Timed'
        self.isViewChanged = False

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(500)
        self.timer.timeout.connect (self.updateMessage)

        #self.isChat.toggle()

        # This variable is derived from Login class of temp
        self.sessionid = str(master.sessionid)

        cookies = {'sessionid':self.sessionid}
        url = 'http://localhost:8000/polls/GetUserDetail'
        r=requests.get(url, cookies=cookies)
        self.username = str(r.text).split()[0]
        self.textBrowser.setText(r.text)

        self.timer.start()

    def reset(self):
    	self.textArea.setText('')

    def submit(self):
        payload={'name':self.username, 'message':str(self.textArea.toPlainText()).strip()}
        if str(self.textArea.toPlainText()).strip() is not '':
            if self.isQues.isChecked():
                payload['isQues'] = True
                payload['isAns' ] = False
            elif self.isAns.isChecked():
                payload['isQues'] = False
                payload['isAns' ] = True
                payload[ 'tag'  ] = str(self.tagArea.toPlainText()).strip()
            else:
                payload['isQues'] = False
                payload['isAns' ] = False
            url = 'http://localhost:8000/polls/PostInsertQuery/'
            data = {'data':json.dumps(payload)}
            r = requests.get(url,params = data)
            # Checks if the request is processed correctly by the server
            if int(r.status_code) == 500:
                d = Dialog ('Invalid Tag Number! Please Try Again..',self)
                d.show()
                self.tagArea.clear()
            else:
                self.textArea.setText('')
            # updates the messages retrived from the server
            self.updateMessage()

    def changeViewToTimed (self):
        self.menuThreaded.setChecked (False)
        self.currentView = 'Timed'
        self.isViewChanged = True
        pass

    def changeViewToThreaded (self):
        self.menuTimed.setChecked (False)
        self.currentView = 'Threaded'
        self.isViewChanged = True
        pass

   
    def updateMessage(self):
        url = 'http://localhost:8000/polls/GetInsertQuery/'
        original =  str(self.textBrowser.toPlainText()).strip()
        # state can be threaded for threaded view or timed for timestamp view
        # give state = timed for timestamp view and any other value for threaded view
        payload = {'data' : str(original[-50:]), 'state' : self.currentView}
        message = str(requests.get(url, params=payload).text).strip()
        # This is checking and updating the messages only when there is a change
        if original != message or self.isViewChanged is True:
            self.isViewChanged = False
    	    self.textBrowser.setText(message)
            # Moves the scroll to the bottom
            self.textBrowser.moveCursor(QtGui.QTextCursor.End)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    chat = Chat()
    chat.show()
    sys.exit(app.exec_())
