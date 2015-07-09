from django.shortcuts import render
from django.http import HttpResponse
from polls.models import *
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from operator import itemgetter
import requests
import datetime
import json


isPlay = False
videoTime = 0
haveQues = False
synVideo = True
isStopped = False

def index (request):
    return HttpResponse("you reached index")

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
    global videoTime, isPlay, haveQues, synVideo, isStopped

    options = []
    if haveQues == False:
        data = {
            'curTime':videoTime,
            'isPlaying':isPlay,
            'haveQues':haveQues,
            'synVideo':synVideo,
            'isStopped':isStopped
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
    global videoTime, isPlay, synVideo, isStopped
    data = str(request.GET['data'])
    data = json.loads(data)
    videoTime = data['currentPosition']
    synVideo = data['synVideo']
    isPlay = not data['isPaused']
    isStopped = data['isStopped']
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
        q = Post.objects.all().order_by('-id')[0]
        if str(q.fromUser) == name and q.timestamp + datetime.timedelta(minutes=3) > timezone.now() and not q.isQues:
            q.message += '\n' + message
            q.timestamp = timezone.now()
            q.save()
        else:
            q = Post(message = message, fromUser = name, timestamp = timezone.now())
    q.save()
    return HttpResponse(name)

def GetInsertQuery (request):
    s = ''
    data = str (request.GET['data'])
    # state can be either threaded or timed..
    state = str (request.GET['state'])

    #lastpostid = 0
    #lastcommentid = 0
    # This is the temporary timestamp view

    if state == 'Threaded':
        for i in Post.objects.all():
            if i.isQues == True:
                s += 'Q' + str(i.id) + ' ' + str(i.fromUser) + ':\n' + str(i.message) + '\n'
                for j in i.comment_set.all():
                    s += 'A' + str(i.id) + ' ' + str(j.fromUser) + ':\n' + str(j.message) + '\n'
            #else:
                #if state == 'Timed':
                    #s += str(i.fromUser) + ':\n' + str(i.message) + '\n'
    elif state == 'Timed':
        a = []
        for i in Post.objects.all():
            b = {}
            b['id'] = i.id
            b['message'] = i.message
            b['fromUser'] = i.fromUser
            b['timestamp'] = i.timestamp
            b['isQues'] = i.isQues
            a.append(b)
        for i in Comment.objects.all():
            b={}
            b['id'] = i.post.id
            b['message'] = i.message
            b['timestamp'] = i.timestamp
            b['fromUser'] = i.fromUser
            b['isQues'] = False
            b['isAns'] = True
            a.append(b)
        # Sort the combined list using the key 'timestamp'
        sortedList = sorted (a, key=itemgetter('timestamp'))
        s = ''
        for i in sortedList:
            if i['isQues'] == True:
                s += 'Q' + str(i['id']) + ' ' + str(i['fromUser']) + ':\n' + str(i['message']) + '\n'
            elif i['isQues'] is False and i.has_key('isAns') and i['isAns'] is True:
                s += 'A' + str(i['id']) + ' ' + str(i['fromUser']) + ':\n' + str(i['message']) + '\n'
            else:
                s += str(i['fromUser']) + ':\n' + str(i['message']) + '\n'


    return HttpResponse(str(s).strip())

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


