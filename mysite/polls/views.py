from django.shortcuts import render
from django.http import HttpResponse
from polls.models import *
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
import requests
import json


isPlay = False
videoTime = 0
haveQues = False
synVideo = True

def index (request):
    return HttpResponse("you reached index")

#def Play (request):
#    global isPlay 
#    isPlay = True
#    return HttpResponse(isPlay)
#
#def Pause (request):
#    global isPlay
#    isPlay = False
#    return HttpResponse(isPlay)
#
#def SetTime (request):   
#    global videoTime
#    videoTime = request.GET['currentposition']
#    return HttpResponse(videoTime)
#
def PostQues (request):   
    global haveQues
    question = str( request.GET['ques'] )
    options  = request.GET.getlist('options')
    curAns   = request.GET.getlist('currectAnswer')

    q = Question(question_text = question, pub_date = timezone.now())
    q.save()

    i=0
    for option in options:
        if curAns[i] == 'True':
            q.choice_set.create(choice_text = str(option), isCurrect=True)
        else:
            q.choice_set.create(choice_text = str(option), isCurrect=False)
        i+=1

    haveQues = True
    return HttpResponse(haveQues)


def SubAns (request):
    submitedAns = request.GET.getlist('options')
    q = Question.objects.order_by('-id')[0]

    options = []
    for option in q.choice_set.all():
        options.append(str(option.isCurrect))

    if options == submitedAns:
        return HttpResponse(True)   #correct response
    else:
        return HttpResponse(False)  #incorrect response

def GetCurSet (request):
    global videoTime, isPlay, haveQues, synVideo

    options = []
    if haveQues == False:
        data = {
            'curTime':videoTime,
            'isPlaying':isPlay,
            'haveQues':haveQues,
            'synVideo':synVideo
        }
    else:
        q = Question.objects.order_by('-id')[0]
        ques_text = str(q.question_text)
        for option in q.choice_set.all():
            options.append(str(option.choice_text))
  
        data = {
            'curTime':videoTime,
            'isPlaying':isPlay,
            'haveQues':haveQues,
            'synVideo':synVideo,
            'question':ques_text,
            'options':options
        }
        haveQues = False
    data2 = json.dumps(data)
    return HttpResponse(data2)

def PostCurSet (request):
    global videoTime, isPlay, haveQues, synVideo
    data = str(request.GET['data'])
    data = json.loads(data)
    videoTime = data['currentPosition']
    synVideo = data['synVideo']
    isPlay = not data['isPaused']
#   haveQues = data['hasQues']
#   if haveQues:
#       question = str( data['ques'] )
#       options  = data['options']
#       curAns   = data['currectAnswer']
#   
#       q = Question(question_text = question, pub_date = timezone.now())
#       q.save()
#   
#       i=0
#       for option in options:
#           if curAns[i]:
#               q.choice_set.create(choice_text = str(option), isCurrect=True)
#           else:
#               q.choice_set.create(choice_text = str(option), isCurrect=False)
#           i+=1
#   
#       haveQues = True
    return HttpResponse('All is well') 
   

def PostInsertQuery (request):
    data = str(request.GET['data'])     # retrieving the data form the GET dictionary
    data = json.loads(data)

    message = str(data['message'])
    name    = str(data['name'   ])
    isQues  = str(data['isQues' ])
    isAns   = str(data['isAns'  ])
    # creating a new Post to save the data in database
    if isQues == 'True':
        q = Post(message = message, fromUser = name, timestamp = timezone.now(), isQues = True)
    elif isAns == 'True':
        tag = data['tag']
        q = Post.objects.get(id=tag) 
        q.comment_set.create(message = message, fromUser = name, timestamp = timezone.now())
    else:
        q = Post(message = message, fromUser = name, timestamp = timezone.now())
    q.save()
    return HttpResponse(name)

def GetInsertQuery (request):
    s = ''
    for post in Post.objects.all().order_by('timestamp'):
        if post.isQues == True:
            s += 'Q' + str(post.id) + ' ' + str(post.fromUser) + ':\n' + str(post.message) + '\n'
            for ans in post.comment_set.all().order_by('timestamp'):
                s += str(ans.fromUser) + ':\n' + str(ans.message) + '\n'
        else:
            s += str(post.fromUser) + ':\n' + str(post.message) + '\n'
    s+='\n'

    return HttpResponse(str(s))

def Register (request):
    # Duplicate Users Integrity Error can be checked using status_code of r
    username = str(request.GET['username'])
    password = str(request.GET[ 'pass'   ])
    email    = str(request.GET[ 'email'  ])
    fname    = str(request.GET[ 'fname'  ])
    lname    = str(request.GET[ 'lname'  ])
    ista     = str(request.GET[ 'ista'   ])

    user = User.objects.create_user(username, email, password)
    user.last_name = lname
    user.first_name = fname
    user.save()
    ta = Group.objects.get(name='TA')
    student = Group.objects.get(name='Student')
    if ista == 'True':
        ta.user_set.add(user)
    else:
        student.user_set.add(user)
    return HttpResponse(username)

def Login (request):
    username = str(request.GET['username'])
    password = str(request.GET['pass'])
    user = authenticate (username=username, password=password)
    if user is not None:
        login (request, user)
        data = {'uname':username}
        data2 = json.dumps(data)
        return HttpResponse(data2)
    else:
        return HttpResponse('')

def GetUserDetail (request):
    u = request.user
    if request.user.is_authenticated() == True:
        return HttpResponse(str(u.username) + '\n' + str(u.email) + '\n' + str(u.first_name) + ' ' + str(u.last_name))
    else:
        return HttpResponse('no user logged in!')

def Logout (request):
    if request.user.is_authenticated():
        logout(request)
    return HttpResponse('')


