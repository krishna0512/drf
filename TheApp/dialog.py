import sys
from StringIO import StringIO
from PyQt4 import QtGui, QtCore, uic

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
