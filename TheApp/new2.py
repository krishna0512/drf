import sys
from PyQt4 import QtGui


class Example(QtGui.QWidget):
        
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
        
    def initUI(self):
        self.i=0
        self.option = []
        self.question = []
        self.optionEdit = []
        self.questionEdit = []
        
        self.question.append(QtGui.QLabel('Question'))
        self.option.append(QtGui.QLabel('Option'))
        
        self.questionEdit.append(QtGui.QLineEdit())
        self.optionEdit.append(QtGui.QLineEdit())

        self.addOptButton = QtGui.QPushButton('',self)
        self.addOptButton.setIcon(QtGui.QIcon('add.png'))
        self.addOptButton.clicked.connect(self.addOption)
        
        self.submitButton = QtGui.QPushButton('Submit',self)
        self.submitButton.clicked.connect(self.submit)
        
        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(10)
        
        self.grid.addWidget(self.question[self.i], 1, 0)
        self.grid.addWidget(self.questionEdit[self.i], 1, 1,1,3)

        self.grid.addWidget(self.option[self.i], 2, 0)
        self.grid.addWidget(self.optionEdit[self.i], 2, 1,1,2)

        self.grid.addWidget(self.addOptButton, 2,3)
        self.grid.addWidget(self.submitButton, 3,2,1,2)
        self.i+=1

        
        self.setLayout(self.grid) 
        
#       self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Review')   

    def addOption(self):
        self.option.append(QtGui.QLabel('Option'))
        self.optionEdit.append(QtGui.QLineEdit())
        self.grid.addWidget(self.option[self.i], 2+self.i, 0)
        self.grid.addWidget(self.optionEdit[self.i],2+self.i,1,1,2)
        self.grid.addWidget(self.addOptButton, 2+self.i,3)
        self.grid.addWidget(self.submitButton, 3+self.i,2,1,2)
        self.i+=1

    def submit(self):
        data=[]
        for j in xrange(self.i):
            data.append(str(self.optionEdit[j].text()).strip())
            print data[j]       

        
def main():
        
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

