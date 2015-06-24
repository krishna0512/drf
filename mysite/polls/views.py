from django.shortcuts import render
from django.http import HttpResponse
from polls.models import Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
import requests
import json


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
    # retrieving the data form the GET dictionary
    message = str(request.GET['message'])
    name = int(request.GET['name'])
    # creating a new Post to save the data in database
    q = Post(message = message, fromUser = name, timestamp = timezone.now())
    q.save()
    retstring = str(q.fromUser) + ' ' + str(q.timestamp) + '\n' + q.message
    return HttpResponse(retstring)

def GetInsertQuery (request):
    s = ''
    for i in Post.objects.all():
        s += str(i.fromUser) + '\n' + str(i.message) + '\n\n'
    return HttpResponse(str(s))

def Register (request):
    # Duplicate Users Integrity Error can be checked using status_code of r
    username = str(request.GET['username'])
    password = str(request.GET['pass'])
    email = str(request.GET['email'])
    fname = str(request.GET['fname'])
    lname = str(request.GET['lname'])
    user = User.objects.create_user (username, email, password)
    user.last_name = lname
    user.first_name = fname
    user.save()
    return HttpResponse(username)


def Login (request):
    username = str(request.GET['username'])
    password = str(request.GET['pass'])
    user = authenticate (username=username, password=password)
    if user is not None:
        login (request, user)
        return HttpResponse(username)
    else:
        return HttpResponse('')


def GetUserDetail (request):
    u = request.user
    if request.user.is_authenticated():
        return HttpResponse(str(u.username) + '\n' + str(u.email) + '\n' + str(u.first_name) + '\n' + str(u.last_name))
    else:
        return HttpResponse('')

def Logout (request):
    if request.user.is_authenticated():
        logout(request)
    return HttpResponse('')


















