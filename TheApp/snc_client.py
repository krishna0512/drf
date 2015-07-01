import sys
import vlc
import pycurl
import requests
import json
from StringIO import StringIO
from PyQt4 import QtGui, QtCore, uic

form_class = uic.loadUiType("clientUi.ui")[0]


class PopupQues(QtGui.QWidget):
        
    def __init__(self,master=None):
        QtGui.QWidget.__init__(self, master)
        lbl1 = QtGui.QLabel(master.question, self)
        lbl1.move(15, 10)
        cb=[]
        for i in xrange(len(master.options)):
            cb.append(QtGui.QCheckBox(master.options[i], self))
            cb[i].move(20, 20+20*i)
            cb[i].toggle()
            cb[i].stateChanged.connect(self.changeTitle)
        self.setGeometry(300, 300, 250, 150)
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
        
    def changeTitle(self, state):
        if state == QtCore.Qt.Checked:
            self.setWindowTitle('QtGui.QCheckBox')
        else:
            self.setWindowTitle('')




class Player(QtGui.QMainWindow,form_class):
    """A simple Media Player using VLC and Qt
    """
    def __init__(self, master=None):
        QtGui.QMainWindow.__init__(self, master)
        self.setupUi(self)
        self.setWindowTitle("Media Player")

        # creating a basic vlc instance
        self.instance = vlc.Instance()
        # creating an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()
        self.isPaused = False
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(200)

        # Connection setups
        self.menuOpen.triggered.connect(self.openFile)
        self.timer.timeout.connect(self.updateUI)
        self.volumeslider.setValue(self.mediaplayer.audio_get_volume())
        self.volumeslider.valueChanged.connect(self.setVolume)

        #global variables
        self.data = {}
        self.isPlaying = False
        self.curPosition = 0
        self.previousStatus = ''
        self.haveQues = False
        self.QuesSet = []

        if self.mediaplayer.play() == -1:
            self.playbutton.setText("Open")

    def setPosition (self, position):
        self.mediaplayer.set_position(position/1000.0)


    def openFile(self, filename=None):
        """Open a media file in a MediaPlayer
        """
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
        self.playbutton.setText("Play")
        self.timer.start()


    def stop(self):
        """Stop player
        """
        self.mediaplayer.stop()
        self.playbutton.setText("Play")


    def setVolume(self, Volume):
        """Set the volume
        """
        self.mediaplayer.audio_set_volume(Volume)

    def playPause(self):
        """Toggle play/pause status (can only be used for client side.)
        """
        status = str(self.isPlaying)

        if status != self.previousStatus:
            if (status == 'True'):
                if self.mediaplayer.play() == -1:
                    self.openFile()
                    return
                self.mediaplayer.play()
                self.playbutton.setText("Pause")
                self.isPaused = False
            else:
                self.mediaplayer.pause()
                self.playbutton.setText("Play")
                self.isPaused = True
        self.previousStatus = status

    def popupExit(self):
        print 'exit'

    def updatePosition (self):
        curPos=self.mediaplayer.get_position()*1000
        buffer = StringIO()
        #getting the position of the server video
        a = float(self.curPosition)
        if (a != ''):
            #a = int(a)
            a=a
        else:
            a=0
        #print str(curPos)+' '+str(a/10)
        if abs(curPos-a/10)>=4.5:
            self.setPosition(a/10)
        #self.mediaplayer.set_time(length*self.mediaplayer.get_position())

    def updateUI(self):
        """updates the user interface"""
        # setting the slider to the desired position
        url = 'http://localhost:8000/polls/GetCurSet/'
        r=requests.get(url)
        self.data = json.loads(r.text)
        self.isPlaying = self.data['isPlaying']
        self.curPosition = self.data['curTime']
        self.haveQues = self.data['haveQues']

        if self.haveQues:
            # self.isPlaying = False
            self.question = self.data['question']
            self.options = self.data['options']
            self.popup = PopupQues(self)
            self.popup.show()


        self.updatePosition()
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
                curTime = str(hour)+':'+str(minute if minute>=10 else '0'+str(minute))+':'+str(sec if sec>=10 else '0'+str(sec))
            else:
                curTime = str(minute if minute>=10 else '0'+str(minute))+':'+str(sec if sec>=10 else '0'+ str(sec))
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
                fullTime = str(hour)+':'+str(minute if minute>=10 else '0'+ str(minute))+':'+str(sec if sec>=10 else '0' + str(sec))
            else:
                fullTime = str(minute if minute>=10 else '0' + str(minute))+':'+str(sec if sec>=10 else '0' + str(sec))
        self.fulltime.setText(fullTime)

        if not self.mediaplayer.is_playing():
            # no need to call this function if nothing is played
            if not self.isPaused:
                # after the video finished, the play button stills show
                # "Pause", not the desired behavior of a media player
                # this will fix it
                self.stop()
        self.playPause()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    player = Player()
    player.show()
    player.resize(640,600)
    if sys.argv[1:]:
        player.openFile(sys.argv[1])
    sys.exit(app.exec_())
