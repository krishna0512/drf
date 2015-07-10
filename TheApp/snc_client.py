import sys
import os
import vlc
import pycurl
import requests
import json
from   dialog     import Dialog
from   random     import randint
from   StringIO   import StringIO
from   PyQt4      import QtGui, QtCore, uic

form_class = uic.loadUiType("clientUi.ui")[0]


class PopupQues(QtGui.QDialog):
    '''
        A simple class to present question to check presence
    '''
    def __init__(self,master=None):
        QtGui.QMainWindow.__init__(self, master)
        self.lbl1 = QtGui.QLabel(str(master.question), self)
        self.cb=[]

        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(10)

        self.grid.addWidget(self.lbl1,1,1,1,6)
        
        for i in xrange(len(master.options)):
            self.cb.append(QtGui.QCheckBox(str(master.options[i]), self))
            self.grid.addWidget(self.cb[i],2+i,2,1,5)
        
        self.submitButton = QtGui.QPushButton('Submit',self)
        self.grid.addWidget(self.submitButton,3+i,3)    
        self.submitButton.clicked.connect(self.submit)

        self.setLayout(self.grid) 
        self.setWindowTitle('tu bheta ye ki nahiiiii ?!!')
        
    def submit(self):
        submitedAns=[]
        for i in xrange(len(self.cb)):
            if self.cb[i].isChecked():
                submitedAns.append(True)
            else:
                submitedAns.append(False)
        url = 'http://localhost:8000/polls/SubAns/'
        payload = {'options':submitedAns}
        r=requests.get(url,params=payload)
        self.hide()

#   def closeEvent(self, event):
#       reply = QtGui.QMessageBox.question(self, 'Message',
#           "Are you sure to quit?", QtGui.QMessageBox.Yes | 
#           QtGui.QMessageBox.No, QtGui.QMessageBox.No)

#       if reply == QtGui.QMessageBox.Yes:
#           #master.isPlaying = master.data['isPlaying']
#           event.accept()
#       else:
#           event.ignore() 
#       



class Player(QtGui.QMainWindow,form_class):
    """A simple Media Player using VLC and Qt for client side
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
        self.playbutton.clicked.connect(self.asynPlay)
        self.stopbutton.clicked.connect(self.stop)
        self.playbutton.setIcon(QtGui.QIcon('playButton.png'))
        self.playbutton.setIconSize(QtCore.QSize(24,24))
        self.stopbutton.setIcon(QtGui.QIcon('stopButton.png'))
        self.stopbutton.setIconSize(QtCore.QSize(24,24))
        self.volumeslider.setValue(self.mediaplayer.audio_get_volume())
        self.volumeslider.valueChanged.connect(self.setVolume)
        self.menuOpen.triggered.connect(self.openFile)
        self.menuExit.triggered.connect(sys.exit)

        #variables
        self.data = {}
        self.isPlaying = False
        self.isPaused = False
        self.isStopped = False
        self.haveQues = False
        self.sync = False
        self.Play = True
        self.curPosition = 0
        self.previousStatus = ''
        self.lastState = ''
        self.QuesSet = []

        if self.mediaplayer.play() == -1:
            self.playbutton.setText("Open")

    def setPosition (self, position):
        self.mediaplayer.set_position(position/1000.0)


    def openFile(self, filename=None):
        """Open a media file in a MediaPlayer
        """
        print 'in openfile'
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


    def keyPressEvent (self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Space:
            self.playbutton.animateClick()
#       if key == QtCore.Qt.Key_Up:
#           volume = int(self.mediaplayer.audio_get_volue())
#           setVolume(volume+5)
#       if key == QtCore.Qt.Key_Down:
#           volume = int(self.mediaplayer.audio_get_volue())
#           setVolume(volume-5)
#       if key == QtCore.Qt.Key_Left:
#           if self.sync == True:
#               position = int(self.mediaplayer.get_position()*1000)
#               setPosition(position + 1000)
#       if key == QtCore.Qt.Key_Right:
#           if self.sync == True:
#               position = int(self.mediaplayer.get_position()*1000)
#               if position > 1000:
#                   setPosition(position - 1000)
    
    def stop(self):
        """Stop player
        """
        print 'in stop'
        self.mediaplayer.stop()
        self.playbutton.setText("Play")


    def setVolume(self, Volume):
        """Set the volume
        """
        self.mediaplayer.audio_set_volume(Volume)

    def playPause(self):
        """Toggle play/pause status (can only be used for client side.)
        """
        print 'play pause'
        if self.Play:
            print 1
            if self.mediaplayer.play() == -1:
                self.openFile()
                return
            self.mediaplayer.play()
            self.playbutton.setText("Pause")
            self.playbutton.setIcon(QtGui.QIcon('pauseButton.png'))
            self.playbutton.setIconSize(QtCore.QSize(24,24))
            self.isPaused = False
        else :
            print 2
            self.mediaplayer.pause()
            self.playbutton.setText("Play")
            self.playbutton.setIcon(QtGui.QIcon('playButton.png'))
            self.playbutton.setIconSize(QtCore.QSize(24,24))
            self.isPaused = True

    def asynPlay(self):
        if not self.sync:
            self.isPaused = not self.isPaused
            self.Play = not self.isPaused
            self.playPause()


    def popupExit(self):
        print 'exit'

    def updatePosition (self):
#       print 'in updatePosition'
        curPos=self.mediaplayer.get_position()*1000
        buffer = StringIO()
        #getting the position of the server video
        a = float(self.curPosition)
        if (a != ''):
            a=a
        else:
            a=0
        if abs(curPos-a/10)>=4.5:
            self.setPosition(a/10)
        #self.mediaplayer.set_time(length*self.mediaplayer.get_position())

    def updateUI(self):
        """updates the user interface"""
        # setting the slider to the desired position
        url = 'http://localhost:8000/polls/GetCurSet/'
        r=requests.get(url)
        self.data        = json.loads(r.text)
        self.sync        = self.data['synVideo' ]
        self.isPlaying   = self.data['isPlaying']
        self.isStopped   = self.data['isStopped']
        self.curPosition = self.data['curTime'  ]
        self.haveQues    = self.data['haveQues' ]

        if self.sync:
            self.Play = self.isPlaying
            self.isPaused = not self.isPlaying
            self.updatePosition()
            if self.isStopped:
                self.stop()
        
        if self.haveQues:
            # self.isPlaying = False
            self.question = self.data['question']
            self.options  = self.data['options' ]
            self.popup = PopupQues(self)
            self.popup.show()


        self.timeslider.setValue(self.mediaplayer.get_position() * 1000)
        #displaying the current time of the video
        curTime=self.mediaplayer.get_time()/1000
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
        self.watchedtime.setText(curTime)
        #displaying the full length of the video
        fullTime=self.mediaplayer.get_length()/1000
        if not fullTime >=0:
            fullTime = str(-1)
        else:
            sec=fullTime%60
            minute=fullTime/60
            if minute>=60:
                minute=minute%60
                hour=minute/60
                minute = str(minute if minute>=10 else '0'+str(minute))
                sec = str(sec if sec>=10 else '0'+str(sec))
                fullTime = str(hour) +':'+ minute +':'+ sec
            else:
                minute = str(minute if minute>=10 else '0'+str(minute))
                sec = str(sec if sec>=10 else '0'+ str(sec))
                fullTime = minute + ':' + sec 
        self.fulltime.setText(fullTime)

        if (self.isPlaying != self.previousStatus or self.sync != self.lastState) and self.sync:
            self.playPause()

        self.previousStatus = self.isPlaying
        self.lastState = self.sync

        if not self.mediaplayer.is_playing():
            # no need to call this function if nothing is played
            if not self.isPaused:
                # after the video finished, the play button stills show
                # "Pause", not the desired behavior of a media player
                # this will fix it
                self.stop()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    player = Player()
    player.show()
    player.resize(640,600)
    if sys.argv[1:]:
        player.openFile(sys.argv[1])
    sys.exit(app.exec_())
