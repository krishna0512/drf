from django.conf.urls import url

from views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^isPlaying/$', isPlaying, name='isPlaying'),
    url(r'^Play/$', Play, name='Play'),
    url(r'^Pause/$', Pause, name='Pause'),
    url(r'^SetTime/(?P<timeStamp>[0-9]+)/$', SetTime, name='SetTime'),
    url(r'^GetTime/$', GetTime, name='GetTime'),
    url(r'^PostInsertQuery/', PostInsertQuery, name='PostInsertQuery'),
    url(r'^GetInsertQuery/', GetInsertQuery, name='GetInsertQuery'),
    url(r'^Register/', Register, name='Register'),
    url(r'^Login/', Login, name='Login'),
    url(r'^GetUserDetail/', GetUserDetail, name='GetUserDetail'),
    url(r'^Logout/', Logout, name='Logout')
]
