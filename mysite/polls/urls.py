from django.conf.urls import url

from views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^isPlaying/$', isPlaying, name='isPlaying'),
    url(r'^Play/$', Play, name='Play'),
    url(r'^Pause/$', Pause, name='Pause'),
    url(r'^SetTime/(?P<timeStamp>[0-9]+)/$', SetTime, name='SetTime'),
    url(r'^GetTime/$', GetTime, name='GetTime'),
    url(r'^GetInsertQuery/(?P<userName>[0-9a-zA-Z]*)/(?P<message>[?!^ +$]^.+)/$', GetInsertQuery, name='GetInsertQuery')
]
