from django.shortcuts import render
from django.http import HttpResponse
from polls.models import Post, Comment
from django.utils import timezone
import requests


isPlay = False
videoTime = 0

def index (request):
    return HttpResponse("you reached index")

def Play (request):
    global isPlay 
    isPlay = True
    return HttpResponse(isPlay)

def Pause (request):
    global isPlay
    isPlay = False
    return HttpResponse(isPlay)

def isPlaying (request):
    global isPlay
    return HttpResponse(isPlay)

def SetTime (request, timeStamp):   
    global videoTime
    videoTime = timeStamp
    return HttpResponse(videoTime)

def GetTime (request):   
    global videoTime
    x = request.GET.has_key('krishna')
    if x:
        return HttpResponse(str( request.GET['krishna']))
    else:
        return HttpResponse("no")

def PostInsertQuery (request):
    q = Post(message = str(request.GET['message']), fromUser = int(request.GET['name']), timestamp = timezone.now())
    q.save()
    return HttpResponse(str(q.fromUser) + ' ' + str(q.timestamp) + '\n' + q.message)

def GetInsertQuery (request):
    s = ''
    for i in Post.objects.all():
        s += str(i.fromUser) + '\n' + str(i.message) + '\n\n'
    return HttpResponse(str(s))
