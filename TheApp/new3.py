
import sys
import vlc
import pycurl
import requests
import json
from StringIO import StringIO
from PyQt4 import QtGui, QtCore, uic
class PopupQues(QtGui.QWidget):
        
    def __init__(self,master=None):
        QtGui.QWidget.__init__(self, master)
        lbl1 = QtGui.QLabel('master.question', self)
        #lbl1.move(15, 10)
        cb=[]
        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(15)
        self.grid.addWidget(lbl1,1,0,1,3)
        for i in xrange(3):
            cb.append(QtGui.QCheckBox('master.options', self))
            #cb[i].move(20, 20+20*i)
            #cb[i].stateChanged.connect(self.changeTitle)
            self.grid.addWidget(cb[i],2+i,1,1,2)



        self.setLayout(self.grid)
        #self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('QtGui.QCheckBox')
        #self.ishow()
    
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            master.isPlaying = master.data['isPlaying']
            event.accept()
        else:
            event.ignore() 
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    es=PopupQues()
    es.show()
    sys.exit(app.exec_())
