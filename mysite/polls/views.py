from django.shortcuts import render
from django.http import HttpResponse
from polls.models import Post, Comment

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
    return HttpResponse(videoTime)

def GetInsertQuery(request,userName,message):
    q = Post(message = str(message), fromUser = int(userName), timestamp = timezone.now())
    q.save()
    return HttpResponse(str(q.message + ' ' + q.fromUser + ' ' + q.timestamp))
    #return HttpResponse(str(userName+Message))
# Create your views here.
