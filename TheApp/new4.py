import sys
import vlc
import pycurl
import requests
import json
from dialog import Dialog
from random import randint
from StringIO import StringIO
from PyQt4 import QtGui, QtCore, uic

class CustomSlider(QtGui.QWidget):
    def __init__(self, minVal=0.0, maxVal=1.0, default=0.0):
        super(CustomSlider, self).__init__()

        self.slider = QtGui.QSlider()
        self.slider.setRange(0.0, 100.0)  # <--
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: black;
                height: 40px;
            }

            QSlider::sub-page:horizontal {
                background: grey;
                height: 40px;
            }

            QSlider::add-page:horizontal {
                background: black;
                height: 40px;
            }""")
        self.overlay = QtGui.QLabel()
        self.overlay.setText("LABEL")
        self.overlay.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.overlay.setStyleSheet("""QLabel{font: bold 18px;color:red;}""")
        self.overlay.mousePressEvent = self.slider.mousePressEvent     # <--
        self.overlay.mouseReleaseEvent = self.slider.mouseReleaseEvent # <--
        self.layout = QtGui.QStackedLayout()
        self.layout.setStackingMode(QtGui.QStackedLayout.StackAll)
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.overlay) 

        self.setLayout(self.layout)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    player = CustomSlider()
    player.show()
    #player.resize(640,600)
    if sys.argv[1:]:
        player.openFile(sys.argv[1])
    sys.exit(app.exec_())
