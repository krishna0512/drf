import sys
import os.path
import requests
from StringIO import StringIO
from PyQt4 import QtGui, QtCore, uic

form_class = uic.loadUiType("temp2.ui")[0]

class Chat(QtGui.QMainWindow,form_class):
    """A simple Media Player using VLC and Qt
    """
    def __init__(self, master=None):
        QtGui.QMainWindow.__init__(self, master)
        self.setupUi(self)
        self.setWindowTitle("Chat Window")

        self.submitButton.clicked.connect(self.submit)
        self.resetButton.clicked.connect(self.reset)

    def reset(self):
    	self.textArea.setText('')

    def submit(self):
        payload={'name':12,'message':str(self.textArea.toPlainText())}
        url = 'http://localhost:8000/polls/PostInsertQuery/'
        r=requests.get(url,params=payload)
        # updates the messages retrived from the server
        self.updateMessage()
   
    def updateMessage(self):
        # Get all the messages from the database
        url = 'http://localhost:8000/polls/GetInsertQuery/'
        message=str(requests.get(url).text)

    	self.textBrowser.setText(message)
    	self.textArea.setText('')

        # Moves the scroll to the bottom
    	self.textBrowser.moveCursor(QtGui.QTextCursor.End)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    chat = Chat()
    chat.show()
    sys.exit(app.exec_())
