import pycurl
import requests
from StringIO import StringIO
name = raw_input ('name: ')
mess = raw_input ('mess: ')
name = int(name)
payload={'name':12,'message':mess}
url = 'http://localhost:8000/polls/PostInsertQuery/'
r=requests.get(url,params=payload)
print r.text
# Body is a string in some encoding.
# In Python 2,
