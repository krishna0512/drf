import sys
import os.path
import requests
import json
from dialog import Dialog
from StringIO import StringIO
from PyQt4 import QtGui, QtCore, uic

form_class = uic.loadUiType("chat.ui")[0]

class Chat(QtGui.QMainWindow,form_class):
    """
        A simple chat box
    """
    def __init__(self, master=None, isTA=False):
        QtGui.QMainWindow.__init__(self, master)
        self.setupUi(self)
        self.setWindowTitle("Chat Window")

        self.submitButton.clicked.connect(self.submit)
        self.resetButton.clicked.connect(self.reset)
        self.menuTimed.triggered.connect(self.changeViewToTimed)
        self.menuThreaded.triggered.connect(self.changeViewToThreaded)
        self.menuExit.triggered.connect(sys.exit)
        self.searchArea.returnPressed.connect(self.search)
        self.currentView = 'Timed'
        self.testBrowser.setVisible(False)
        self.isViewChanged = False

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect (self.updateMessage)

        self.isChat.toggle()
        self.qwqw = 0
        self.wqwq = 0
        # This variable is derived from Login class of temp
        
        self.sessionid = str(master.sessionid)

        cookies = {'sessionid':self.sessionid}
        url = 'http://localhost:8000/polls/GetUserDetail/'
        r=requests.get(url, cookies=cookies)
        self.username = str(r.text).split()[0]
        self.isTA = isTA
        print isTA
        self.textBrowser.setText(r.text)

        self.timer.start()

    def keyPressEvent (self, event):
        mod = QtGui.QApplication.keyboardModifiers()
        if mod == QtCore.Qt.ControlModifier:
            key = event.key()
            if key == QtCore.Qt.Key_Return:
                self.submitButton.animateClick()

    def reset(self):
    	self.textArea.setText('')

    def submit(self):
        m = str(self.textArea.toPlainText()).strip()
        if m.find('@timenow') is not -1:
            url = 'http://localhost:8000/polls/GetCurSet/'
            r = requests.get(url)
            timenow = json.loads(str(r.text))['curTime']
            m = m.replace('@timenow', '<a href="time://' + str(timenow) + '">@' + str(timenow) + '</a>')
        payload={'name':self.username, 'message':m}
        if m is not '':
            if self.isQues.isChecked():
                payload['isQues'] = True
                payload['isAns' ] = False
            elif self.isAns.isChecked():
                payload['isQues'] = False
                payload['isAns' ] = True
                payload[ 'tag'  ] = str(self.tagArea.text()).strip()
            else:
                payload['isQues'] = False
                payload['isAns' ] = False
            url = 'http://localhost:8000/polls/PostInsertQuery/'
            data = {'data':json.dumps(payload)}
            r = requests.get(url,params = data)
            # Checks if the request is processed correctly by the server
            if int(r.status_code) == 500:
                d = Dialog ('Invalid! Please Try Again..',self)
                d.show()
                self.tagArea.clear()
            else:
                self.textArea.setText('')
                self.tagArea.clear()
                self.isChat.setChecked(True)
            # updates the messages retrived from the server
            #self.updateMessage()

    def changeViewToTimed (self):
        self.menuThreaded.setChecked (False)
        self.currentView = 'Timed'
        self.isViewChanged = True
        pass 

    def changeViewToThreaded (self):
        self.menuTimed.setChecked (False)
        self.currentView = 'Threaded'
        self.isViewChanged = True
        pass

    def on_anchor_clicked(self,url):
        text = str(url.toString())
        self.timer.stop()
        print text
        if text.startswith('id_://'):
            self.qwqw += 1
            self.textBrowser.setSource(QtCore.QUrl()) #stops the page from changing
            function = text.replace('id_://','')
            temp = function.split('_',1)
            print temp[0]+'asdaszf '+temp[1]+ '\t\tself.qwqw:' + str(self.qwqw)
            if hasattr(self,temp[1]):
                getattr(self,temp[1])(temp[0])
        elif text.startswith ('time://'):
            self.wqwq += 1
            self.textBrowser.setSource(QtCore.QUrl())
            print "Time sets instruction received."
            t = text.replace ('time://', '')
            print "time = " + t
            data2 = {}
            data2['timed'          ] = True
            data2['chatPos'        ] = int(t)
            payload = json.dumps(data2)
            payload = {'data':payload}
            print payload
            url = 'http://localhost:8000/polls/PostTimedSet/'
            r = requests.get(url,params=payload)
            print str(r.status_code) + '\twqwq:' + str(self.wqwq)
        self.timer.start()

    def a_function(self,no):
        print 'you called?'
        self.tagArea.setText(str(no))
        self.isAns.setChecked(True)
        print 'im leaving >.<'
    
    def c_function(self,no):
        print 'you called?'
        url = 'http://localhost:8000/polls/ComDelete/'
        payload = {'id':no}
        r = requests.get(url,params=payload)
        if r.text == 'deleted':
            print 'finally'
        print 'im leaving >.<'
   
    def b_function(self,no):
        print 'you called?'
        url = 'http://localhost:8000/polls/Delete/'
        payload = {'id':no}
        r = requests.get(url,params=payload)
        if r.text == 'deleted':
            print 'finally'
        print 'im leaving >.<'

    def getAllAnsFor (self, qid):
        url = 'http://localhost:8000/polls/GetInsertQuery/'
        payload = {'state':self.currentView}
        data = json.loads(str(requests.get(url,params=payload).text))
        ans = []
        s=''
        for i in data:
            if i['id'] == qid and i['isAns'] == False:
                ans = i['ans']
        for i in ans:
            s += 'A' + str(qid) + ') ' + str(i['fromUser']) + ':\n'
            s += str(i['message']) + '\n\n'
        return s.strip()

   
    def updateMessage(self):
        url = 'http://localhost:8000/polls/GetInsertQuery/'
        payload = {'state' : self.currentView}
        r = requests.get(url, params=payload)
        m = json.loads(r.text)
        original =  str(self.textBrowser.toHtml()).strip()
        # state can be threaded for threaded view or timed for timestamp view
        # give state = timed for timestamp view and any other value for threaded view
        message = '''<html>
            <head><style type=text/css>
            .ques {color:green; text-decoration:none; font-size: 15pt}
            .ans  {color:blue; font-size:10pt; margin: 0px; padding:0px}
            .del  {color:red; font-size:12pt; text-decoration:none}
            p {margin : 0px; padding: 0px}
            </style></head><body>'''
        if self.currentView == 'Threaded':
            for i in m:
                if i['isQues'] == True:
                    message += '<a class = "ques" href="id_://' + str(i['id']) + '_a_function">'
                    if i['hasAns'] is True:
                        message += '<p title=\'' + self.getAllAnsFor(i['id']) + '\'>'
                       #message += '<p title="Answers are available">'
                    else:
                        message += '<p title="No Answer Available">'
                    message += 'Q' + str(i['id']) + ')' + str(i['fromUser']) + ':</a><br />'
                    message += str(i['message']).replace('\n','<br />') 
                    message += '</p>'
                    if self.isTA:
                        message += '<a class = "del" href="id_://' + str(i['id']) + '_b_function">X</a>'
                    message += '<br><br>'
                    if i['hasAns'] == True:
                        ans = i['ans']
                        for j in ans:
                            message += '<p class="ans" title=\'Q' + str(i['id']) + ') ' + i['fromUser'] + ':\n' + i['message'] + '\'>'
                            message += 'A' + str(j['id']) + ')' + str(j['fromUser']) + ':</p>'
                            message += str(j['message']).replace('\n','<br />')
                            if self.isTA:
                                message += '<a class = "del" href="id_://' + str(j['myId']) + '_c_function">X</a>'
                            message += '<br><br>'
        else: 
            for i in m:
                if i['isQues'] == True:
                    message += '<a class = "ques" href="id_://' + str(i['id']) + '_a_function">'
                    if i['hasAns'] is True:
                        message += '<p title=\'' + self.getAllAnsFor(i['id']) + '\'>'
                       #message += '<p title="Answers are available">'
                    else:
                        message += '<p title="No Answer Available">'
                    message += 'Q' + str(i['id']) + ')' + str(i['fromUser']) + ':</a><br />' 
                    message += str(i['message']).replace('\n','<br />')
                    message += '</p>'
                    if self.isTA:
                        message += '<a class = "del" href="id_://' + str(i['id']) + '_b_function">X</a>'
                    message += '<br><br>'
                elif i['isQues'] is False and i['isAns'] is True:
                    message += '<p class="ans" title=\'Q' + str(i['id']) + ') ' + i['fromUser'] + ':\n' + i['postMessage'] + '\'>'
                    message += 'A' + str(i['id']) + ')' + str(i['fromUser']) + ':</p>'
                    message += str(i['message']).replace('\n','<br />')
                    if self.isTA:
                        message += '<a class = "del" href="id_://' + str(i['myId']) + '_c_function">X</a>'
                    message += '<br><br>'
                else:
                    message += '<p title=\'' + i['fromUser'] + ':\n' + i['message'] + '\'>'
                    message += str(i['fromUser']) + ':<br />'
                    message += str(i['message']).replace('\n','<br />')
                    message += '</p>'
                    if self.isTA:
                        message += '<a class = "del" href="id_://' + str(i['id']) + '_b_function">X</a>'
                    message += '<br><br>'
#       message += '<br />'
        message += '</body></html>'
        self.textBrowser.anchorClicked.connect(self.on_anchor_clicked)
        # This is checking and updating the messages only when there is a change
        # testBrowser is dummy textBrower added in UI to match the newMessage so that scrolling can be effective
        self.testBrowser.setHtml(message)
        newMessage = str(self.testBrowser.toHtml()).strip()
        if str(original).strip() != str(newMessage).strip() or self.isViewChanged is True:
            self.isViewChanged = False
    	    self.textBrowser.setHtml(message)
            # Moves the scroll to the bottom
            self.textBrowser.moveCursor(QtGui.QTextCursor.End)
        
    def search(self):
        if not self.is_number(self.searchArea.text()):
            d = Dialog ('Invalid! Please Try Again..',self)
            d.show()
            self.searchArea.clear()
        else :
            url = 'http://localhost:8000/polls/Search/'
            payload = {'id' : int(self.searchArea.text())}
            r = requests.get(url, params=payload)
            m = json.loads(r.text)
            if int(r.status_code) == 500:
                d = Dialog ('Invalid! Please Try Again..',self)
                d.show()
                self.searchArea.clear()
            else:
                data = json.loads(r.text)
                if data['ques'] == {}:
                    d = Dialog ('Not a question! Please Try Again..',self)
                    d.show()
                    self.searchArea.clear()
                else:
                    message = 'Q '+ str(data['ques']['message'])
                    message += '\n'
                    if data['ques']['hasAns']:
                        ans = data['answer']
                        j = 1
                        for i in ans:
                            message +='A'+str(j)+' '+ i['message']+'\n'
                            j += 1
                    d = Dialog (message,self)
                    d.show()
                    self.searchArea.clear()
                
    def is_number(self,s):
        try:
            int(s)
            return True
        except ValueError:
            return False
        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            cookies = {'sessionid':self.sessionid}
            url = 'http://localhost:8000/polls/Logout/'
            r=requests.get(url, cookies=cookies)
            #r = requests.get(url)
            event.accept()
        else:
            event.ignore() 



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    chat = Chat()
    chat.show()
    sys.exit(app.exec_())
