import sys
from PyQt4 import QtGui, QtCore

class PopupQues(QtGui.QWidget):
        
    def __init__(self,master=None):
        QtGui.QWidget.__init__(self, master)
        lbl1 = QtGui.QLabel('Question appears here', self)
        lbl1.move(15, 10)
        cb=[]
        for i in xrange(0,3):
            cb.append(QtGui.QCheckBox('Show title'+str(i), self))
            cb[i].move(20, 30+20*i)
            cb[i].toggle()
            cb[i].stateChanged.connect(self.changeTitle)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('QtGui.QCheckBox')
        
    def changeTitle(self, state):
        if state == QtCore.Qt.Checked:
            self.setWindowTitle('QtGui.QCheckBox')
        else:
            self.setWindowTitle('')
                                                        
def main():
    app = QtGui.QApplication(sys.argv)
    ex = PopupQues()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
