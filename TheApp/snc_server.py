import sys
import os.path
import vlc
import pycurl
from StringIO import StringIO
from PyQt4 import QtGui, QtCore, uic

form_class = uic.loadUiType("temp.ui")[0]

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
        self.timer.timeout.connect(self.updateUI)
        self.timeslider.sliderMoved.connect(self.setPosition)
        self.playbutton.clicked.connect(self.playPause)
        self.stopbutton.clicked.connect(self.stop)
        self.menuOpen.triggered.connect(self.openFile)
        self.playbutton.setIcon(QtGui.QIcon('playButton.png'))
        self.playbutton.setIconSize(QtCore.QSize(24,24))
        self.stopbutton.setIcon(QtGui.QIcon('stopButton.png'))
        self.stopbutton.setIconSize(QtCore.QSize(24,24))
        self.volumeslider.setValue(self.mediaplayer.audio_get_volume())
        self.volumeslider.valueChanged.connect(self.setVolume)
        #self.menubar.menuOpen.triggered.connect(self.openFile)
        #self.menubar.menuExit.triggered.connect(sys.exit)

        if self.mediaplayer.play() == -1:
            self.playbutton.setText("Open")

    def setPosition (self, position):
        self.mediaplayer.set_position(position/1000.0)


    def openFile(self, filename=None):
        """Open a media file in a MediaPlayer
        """
        if filename == False:
            filename = None
        print 'reached open'
        print filename
        if filename is None:
            filename = QtGui.QFileDialog.getOpenFileName(self, "Open File", os.path.expanduser('~'))
        print filename
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
        self.playPause()


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
        """Toggle play/pause status
        """
        buffer = StringIO()
        c = pycurl.Curl()
        if self.mediaplayer.is_playing():
            c.setopt(c.URL, 'http://localhost:8000/polls/Pause/')
            c.setopt(c.WRITEDATA, buffer)
            c.perform()
            c.close()
            self.mediaplayer.pause()
            self.playbutton.setText("Play")
            self.playbutton.setIcon(QtGui.QIcon('playButton.png'))
            self.playbutton.setIconSize(QtCore.QSize(24,24))
            self.isPaused = True
        else:
            c.setopt(c.URL, 'http://localhost:8000/polls/Play/')
            c.setopt(c.WRITEDATA, buffer)
            c.perform()
            c.close()
            if self.mediaplayer.play() == -1:
                self.openFile()
                return
            self.mediaplayer.play()
            self.playbutton.setText("Pause")
            self.playbutton.setIcon(QtGui.QIcon('pauseButton.png'))
            self.playbutton.setIconSize(QtCore.QSize(24,24))
            self.timer.start()
            self.isPaused = False


    def updateUI(self):
        """updates the user interface"""
        # setting the slider to the desired position
        self.timeslider.setValue(self.mediaplayer.get_position() * 1000)
        curTime=self.mediaplayer.get_time()/1000
        if not curTime >= 0:
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
        fullTime=self.mediaplayer.get_length()/1000
        if not fullTime >=0:
            fullTime=str(-1)
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

        c = pycurl.Curl()
        url = 'http://localhost:8000/polls/SetTime/' + str(int(self.mediaplayer.get_position()*10000)) + '/'
        print 'q'
        #url = 'http://localhost:8000/polls/SetTime/' +str(12) + '/'
        print 'w'
        c.setopt(c.URL, url)
        c.perform()
        c.close()
        if not self.mediaplayer.is_playing():
            # no need to call this function if nothing is played
            self.timer.stop()
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
