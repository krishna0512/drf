import pycurl
from StringIO import StringIO

buffer = StringIO()
c = pycurl.Curl()
name = raw_input('enter user name')
message = raw_input('enter the message')
url = 'http://localhost:8000/polls/GetInsertQuery/'+ str(name) + '/' + str(message) + '/'
c.setopt(c.URL, url)
c.setopt(c.WRITEDATA, buffer)
c.perform()
body = buffer.getvalue()
print body
c.close()
# Body is a string in some encoding.
# In Python 2,
