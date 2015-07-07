import sys
import os.path
import requests
import json
from StringIO import StringIO
from PyQt4 import QtGui, QtCore, uic

form_class = uic.loadUiType("chat.ui")[0]

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

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(500)
        self.timer.timeout.connect (self.updateMessage)

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
        if str(self.textArea.toPlainText()).strip()!='':
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
            requests.get(url,params = data)
            self.textArea.setText('')
            # updates the messages retrived from the server
            self.updateMessage()
   
    def updateMessage(self):
        # Get all the messages from the database
        url = 'http://localhost:8000/polls/GetInsertQuery/'
        message=str(requests.get(url).text)

    	self.textBrowser.setText(message)

        # Moves the scroll to the bottom
    	self.textBrowser.moveCursor(QtGui.QTextCursor.End)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    chat = Chat()
    chat.show()
    sys.exit(app.exec_())
