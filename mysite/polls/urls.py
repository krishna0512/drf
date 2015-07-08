from django.conf.urls import url

from views import *

urlpatterns = [
    url(r'^$', index, name='index'),
#   url(r'^Play/$', Play, name='Play'),
#   url(r'^Pause/$', Pause, name='Pause'),
#   url(r'^SetTime/', SetTime, name='SetTime'),
    url(r'^GetCurSet/', GetCurSet, name='GetCurSet'),
    url(r'^PostCurSet/', PostCurSet, name='PostCurSet'),
    url(r'^PostQues/', PostQues, name='PostQues'),
    url(r'^SubAns/', SubAns, name='SubAns'),
    url(r'^PostInsertQuery/', PostInsertQuery, name='PostInsertQuery'),
    url(r'^GetInsertQuery/', GetInsertQuery, name='GetInsertQuery'),
    url(r'^Register/', Register, name='Register'),
    url(r'^Login/', Login, name='Login'),
    url(r'^GetUserDetail/', GetUserDetail, name='GetUserDetail'),
    url(r'^Logout/', Logout, name='Logout')
]
