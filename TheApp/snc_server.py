import sys
import os.path
import vlc
import pycurl
import json
import requests
from dialog import Dialog
from StringIO import StringIO
from PyQt4 import QtGui, QtCore, uic

form_class = uic.loadUiType("serverUi.ui")[0]

class PostQues(QtGui.QWidget):
    '''
        A simple class for posting popup question to check presence
    '''    
    def __init__(self,master=None):
        QtGui.QWidget.__init__(self, master)
        self.setWindowTitle('Post Question')
        
        self.i=0
        self.option = []
        self.question = []
        self.optionEdit = []
        self.questionEdit = []
        self.currectOption = []

        
        self.question.append(QtGui.QLabel('Question'))
        self.option.append(QtGui.QLabel('Option'+ str(self.i + 1)))
        
        self.questionEdit.append(QtGui.QLineEdit())
        self.optionEdit.append(QtGui.QLineEdit())

        self.addOptButton = QtGui.QPushButton('',self)
        self.addOptButton.setIcon(QtGui.QIcon('add.png'))
        self.addOptButton.clicked.connect(self.addOption)
        
        self.submitButton = QtGui.QPushButton('Submit',self)
        self.submitButton.clicked.connect(self.submit)
            
        self.currectOption.append(QtGui.QCheckBox('',self))
        
        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(10)
        
        self.grid.addWidget(self.question[self.i], 1, 0)
        self.grid.addWidget(self.questionEdit[self.i], 1, 1,1,6)

        self.grid.addWidget(self.option[self.i], 2, 0)
        self.grid.addWidget(self.optionEdit[self.i], 2, 1,1,4)
        self.grid.addWidget(self.currectOption[self.i], 2, 5)
        self.grid.addWidget(self.addOptButton, 2,6)
        
        self.grid.addWidget(self.submitButton, 3,2,1,2)
        self.i+=1

        
        self.setLayout(self.grid) 
        
#       self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Review')   

    def addOption(self):
        self.option.append(QtGui.QLabel('Option'+ str(self.i + 1)))
        self.optionEdit.append(QtGui.QLineEdit())
        self.currectOption.append(QtGui.QCheckBox('',self))
        self.grid.addWidget(self.option[self.i], 2+self.i, 0)
        self.grid.addWidget(self.optionEdit[self.i],2+self.i,1,1,4)
        self.grid.addWidget(self.currectOption[self.i], 2+self.i, 5)
        self.grid.addWidget(self.addOptButton, 2 + self.i, 6)
        self.grid.addWidget(self.submitButton, 3 + self.i, 2, 1, 2)
        self.i+=1

    def submit(self):
        options=[]
        currectAns = []
        question = str(self.questionEdit[0].text()).strip()
        for j in xrange(self.i):
            options.append(str(self.optionEdit[j].text()).strip())    
            if self.currectOption[j].isChecked():
                currectAns.append(True)
            else:
                currectAns.append(False)
        if not question or options[0] == '':
            self.dlg = Dialog("Field missing")
            self.dlg.show()
            
        else:
            url = 'http://localhost:8000/polls/PostQues/'
            payload = {'options':options, 'ques':question, 'currectAnswer':currectAns}
            r=requests.get(url,params=payload)
            self.hide()
    
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore() 
        


class Player(QtGui.QMainWindow,form_class):
    """A simple Media Player using VLC and Qt for server side
    """
    def __init__(self, master=None):
        QtGui.QMainWindow.__init__(self, master)
        self.setupUi(self)
        self.setWindowTitle("Media Player")

        # creating a basic vlc instance
        self.instance = vlc.Instance()
        # creating an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(200)

        # Connection setups
        self.timer.timeout.connect(self.updateUI)
        self.timeslider.sliderMoved.connect(self.setPosition)
        self.playbutton.clicked.connect(self.playPause)
        self.stopbutton.clicked.connect(self.stop)
        self.playbutton.setIcon(QtGui.QIcon('playButton.png'))
        self.playbutton.setIconSize(QtCore.QSize(24,24))
        self.stopbutton.setIcon(QtGui.QIcon('stopButton.png'))
        self.stopbutton.setIconSize(QtCore.QSize(24,24))
        self.volumeslider.setValue(self.mediaplayer.audio_get_volume())
        self.volumeslider.valueChanged.connect(self.setVolume)
        self.menuOpen.triggered.connect(self.openFile)
        self.menuPost.triggered.connect(self.postQues)
        self.menuExit.triggered.connect(sys.exit)

        self.synVideo.toggle()
        
        # Variables
        self.payload = {}
        self.payload['isPaused'] = False
        self.payload['hasQues'] = False
        self.payload['synVideo'] = True
        self.payload['isStopped'] = False

        if self.mediaplayer.play() == -1:
            self.playbutton.setText("Open")

    def keyPressEvent (self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Space:
            self.playbutton.animateClick()
        if key == QtCore.Qt.Key_Up:
            volume = int(self.mediaplayer.audio_get_volue())
            setVolume(volume+5)
        if key == QtCore.Qt.Key_Down:
            volume = int(self.mediaplayer.audio_get_volue())
            setVolume(volume-5)
        if key == QtCore.Qt.Key_Left:
            if self.sync == True:
                position = int(self.mediaplayer.get_position()*1000)
                setPosition(position + 1000)
        if key == QtCore.Qt.Key_Right:
            if self.sync == True:
                position = int(self.mediaplayer.get_position()*1000)
                if position > 1000:
                    setPosition(position - 1000)
    
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            self.payload['synVideo'] = False
            data = json.dumps(self.payload)
            data = {'data':data}
            url = 'http://localhost:8000/polls/PostCurSet/'
            r = requests.get(url,params = data)
            print 'about to exit'
            event.accept()
        else:
            event.ignore() 
        
    def setPosition (self, position):
        self.mediaplayer.set_position(position/1000.0)

    def postQues (self, position):
        self.popup = PostQues()
        self.popup.show()

    def popupExit(self, values):
        self.payload['hasQues'] = True
        for value in values:
            self.payload[value] = values[value]

    def openFile(self, filename=None):
        """Open a media file in a MediaPlayer
        """
        if filename == False:
            filename = None
        if filename is None:
            filename = QtGui.QFileDialog.getOpenFileName(self, "Open File", os.path.expanduser('~'))
        if not filename:
            return

        # create the media
        if sys.version < '3':
            filename = unicode(filename)
        self.media = self.instance.media_new(filename)
        # put the media in the media player
        self.mediaplayer.set_media(self.media)

        # parse the metadata of the file
        self.media.parse()
        # set the title of the track as window title
        self.setWindowTitle(self.media.get_meta(0))

        # the media player has to be 'connected' to the QFrame
        # (otherwise a video would be displayed in it's own window)
        # this is platform specific!
        # you have to give the id of the QFrame (or similar object) to
        # vlc, different platforms have different functions for this
        if sys.platform.startswith('linux'): # for Linux using the X Server
            self.mediaplayer.set_xwindow(self.videoframe.winId())
        elif sys.platform == "win32": # for Windows
            self.mediaplayer.set_hwnd(self.videoframe.winId())
        elif sys.platform == "darwin": # for MacOS
            self.mediaplayer.set_nsobject(self.videoframe.winId())
        self.timer.start()
        self.playbutton.setText("Play")
        self.playPause()


    def stop(self):
        """Stop player
        """
        self.mediaplayer.stop()
        self.playbutton.setText("Play")
        self.payload['isStopped'] = True


    def setVolume(self, Volume):
        """Set the volume
        """
        self.mediaplayer.audio_set_volume(Volume)


    def playPause(self):
        """Toggle play/pause status
        """
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.playbutton.setText("Play")
            self.playbutton.setIcon(QtGui.QIcon('playButton.png'))
            self.playbutton.setIconSize(QtCore.QSize(24,24))
            self.payload['isPaused'] = True
        else:
            if self.mediaplayer.play() == -1:
                self.openFile()
                return
            self.mediaplayer.play()
            self.playbutton.setText("Pause")
            self.playbutton.setIcon(QtGui.QIcon('pauseButton.png'))
            self.playbutton.setIconSize(QtCore.QSize(24,24))
            self.payload['isPaused'] = False
    
    def theTime(self, curTime):
        if not curTime>=0:
            curTime=str(-1)
        else:
            sec=curTime%60
            minute=curTime/60
            if minute>=60:
                minute=minute%60
                hour=minute/60
                minute = str(minute if minute>=10 else '0'+str(minute))
                sec = str(sec if sec>=10 else '0'+str(sec))
                curTime = str(hour) +':'+ minute +':'+ sec
            else:
                minute = str(minute if minute>=10 else '0'+str(minute))
                sec = str(sec if sec>=10 else '0'+ str(sec))
                curTime = minute + ':' + sec 
        return curTime

    def updateUI(self):
        """updates the user interface"""
        # setting the slider to the desired position
        self.timeslider.setValue(self.mediaplayer.get_position() * 1000)
        #displaying the current position of the video
        curTime=self.mediaplayer.get_time()/1000
        self.watchedtime.setText(self.theTime(curTime))
        #displaying the full length of the video
        fullTime=self.mediaplayer.get_length()/1000
        self.fulltime.setText(self.theTime(fullTime))

        if self.synVideo.isChecked():
            self.payload['synVideo'] = True
        else :
            self.payload['synVideo'] = False
        self.payload['currentPosition']=int(self.mediaplayer.get_position()*10000)
        data = json.dumps(self.payload)
        data = {'data':data}
        url = 'http://localhost:8000/polls/PostCurSet/'
        r = requests.get(url,params = data)
        if self.payload['hasQues'] == True:
            self.payload['hasQues'] = False      #   The question has been sent so....
        if not self.mediaplayer.is_playing():    #   Check if somrthing is playing or paused else stop it  
            if not self.payload['isPaused']:
                self.stop()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    player = Player()
    player.show()
    player.resize(640,600)
    if sys.argv[1:]:
        player.openFile(sys.argv[1])
    sys.exit(app.exec_())
