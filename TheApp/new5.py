import sys

from PyQt4 import QtGui
from PyQt4 import QtCore

class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        main_layout = QtGui.QVBoxLayout()
        a='krishna'

        self.browser = QtGui.QTextBrowser()
        self.browser.setHtml('''<html>
            <head><style type=text/css>
            a:link {color:red; text-decoration:none;}
            a:hover {color:blue; text-decoration:underline}
            </style></head>
            <body>some text<br>
            <a href="a23://a_function">click me to call a function</a>
            <br>
            <a href="#my_anchor">'''+' tulsyan' + ''' Click me to scroll down</a>
            <br>foo<br>foo<br>foo<br>foo<br>foo<br>foo<br>
            <a id="my_anchor"></a><br>bar<br>bar<br>bar<br>bar<br>bar<br>bar
            <br>hello!<br>hello!<br>hello!<br>hello!<br>hello!<br>hello!<br>hello!<br>hello!
            </body></html>''')

        self.browser.anchorClicked.connect(self.on_anchor_clicked)

        main_layout.addWidget(self.browser)

        self.setLayout(main_layout)

    def on_anchor_clicked(self,url):
        text = str(url.toString())
        print text
        if text.startswith('a23://'):
            self.browser.setSource(QtCore.QUrl()) #stops the page from changing
            function = text.replace('a23://','')
            if hasattr(self,function):
                getattr(self,function)(1232)

    def a_function(self,no):
        print 'you called?'+str(no)

app = QtGui.QApplication(sys.argv)
window = MainWindow()
window.show()

sys.exit(app.exec_())