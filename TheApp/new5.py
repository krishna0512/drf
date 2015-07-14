import sys

from PyQt4 import QtGui
from PyQt4 import QtCore

class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        main_layout = QtGui.QVBoxLayout()
        self.browser = QtGui.QTextBrowser()
        self.browser.setHtml('''<html>
            <head><style type=text/css>
            a:link {color:green; text-decoration:none;}
            .p1 {color : orange;}
            .qq {color : red; float: right; }
            </style></head>
            <body>some text<br>
            <a href="a23://a_function">click me to call a function</a>
            <br><p title="tootip">some block of text</p>
            <a href="#my_anchor">Click me to scroll down</a>
            <br><p class="p1">foo<br> 
            <table> <tr> <th> X </ th><th> Y</ th></ tr><tr> <td> Xx </ td><td> Yy</ td></ tr><tr> <td> Xxx </ td><td> Yyy</ td></ tr></ table>
            foo<br>foo<br>foo<br>foo<br>foo</p>
            <a id="my_anchor"></a><br>bar<br>bar<br>bar<br>bar<br>bar<br>bar
            <br>hello!<br>hello!<br>hello!<br>hello!<table> <tr> <th class="qq"> X </ th> </ tr></ table><br>hello!<br>hello!<br>hello!<br>hello!
            </body></html>''')

        self.browser.anchorClicked.connect(self.on_anchor_clicked)
        style = '''  
            background-color: red;
            '''
        #self.browser.setStyleSheet(style)
        main_layout.addWidget(self.browser)

        self.setLayout(main_layout)

    def on_anchor_clicked(self,url):
        text = str(url.toString())
        print text
        if text.startswith('a23://'):
            self.browser.setSource(QtCore.QUrl()) #stops the page from changing
            function = text.replace('a23://','')
            if hasattr(self,function):
                getattr(self,function)

    def a_function(self):
        print 'you called?'

app = QtGui.QApplication(sys.argv)
window = MainWindow()
window.show()

sys.exit(app.exec_())
