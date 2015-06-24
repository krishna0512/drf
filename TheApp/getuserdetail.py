import pycurl
import requests
from StringIO import StringIO

url = 'http://localhost:8000/polls/GetUserDetail'
r=requests.get(url)
if r.text == '':
    print "There is no user currently logged in.!"
else:
    for i in r.text.split():
        print i
