from django.shortcuts import render
from django.http import HttpResponse
from polls.models import *
from django.contrib.auth.models import User, Group
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from operator import itemgetter
import requests
import datetime
import json


isPlay = False
videoTime = 0
synVideo = True
isStopped = False
timed = False
haveQues = False
chatPos = 0

def initialise (request):
    request.session['timed'] = False
    request.session['haveQues'] = False
    request.session['chatPos'] = 0
    return HttpResponse("current session time is = " + str(request.session['temp']))

def index (request):
    if not 'temp' in request.session:
        request.session['temp']=0
    request.session['temp'] += 1
    return HttpResponse("current session time is = " + str(request.session['temp']))

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

def GetCurSet2 (request):
    global videoTime, isPlay, haveQues, synVideo, isStopped, timed, chatPos

    options = []
    if haveQues == False:
        data = {
            'curTime'   :videoTime,
            'isPlaying' :isPlay,
            'haveQues'  :haveQues,
            'synVideo'  :synVideo,
            'isStopped' :isStopped,
            'timed'     :timed,
            'chatPos'   :chatPos
        }
    else:
        q = Question.objects.order_by('-id')[0]
        ques_text = str(q.question_text)
        for option in q.choice_set.all():
            options.append(str(option.choice_text))
  
        data = {
            'curTime'   :videoTime,
            'isPlaying' :isPlay,
            'haveQues'  :haveQues,
            'synVideo'  :synVideo,
            'isStopped' :isStopped,
            'question'  :ques_text,
            'options'   :options,
            'timed'     :timed,
            'chatPos'   :chatPos
        }
    #timed = False
    data2 = json.dumps(data)
    return HttpResponse(data2)

def GetCurSet (request):
    global videoTime, isPlay, haveQues, synVideo, isStopped, timed, chatPos

    options = []
    if haveQues == False:
        data = {
            'curTime'   :videoTime,
            'isPlaying' :isPlay,
            'haveQues'  :haveQues,
            'synVideo'  :synVideo,
            'isStopped' :isStopped,
            'timed'     :timed,
            'chatPos'   :chatPos
        }
    else:
        q = Question.objects.order_by('-id')[0]
        ques_text = str(q.question_text)
        for option in q.choice_set.all():
            options.append(str(option.choice_text))
  
        data = {
            'curTime'   :videoTime,
            'isPlaying' :isPlay,
            'haveQues'  :haveQues,
            'synVideo'  :synVideo,
            'isStopped' :isStopped,
            'question'  :ques_text,
            'options'   :options,
            'timed'     :timed,
            'chatPos'   :chatPos
        }
        haveQues = False
    #timed = False
    data2 = json.dumps(data)
    return HttpResponse(data2)

def PostCurSet (request):
    global videoTime, isPlay, synVideo, isStopped, timed, chatPos
    data = str(request.GET['data'])
    data = json.loads(data)
    videoTime   = data['currentPosition']
    synVideo    = data['synVideo'       ]
    isPlay      = not data['isPaused'   ]
    isStopped   = data['isStopped'      ]
    data = {}
    if timed == True:
        data['timed'  ] = True
        data['chatPos'] = chatPos
        timed = False
    else : 
        data['timed'  ] = False
        data['chatPos'] = videoTime
    data = json.dumps(data)
    return HttpResponse(data) 

def PostTimedSet (request):
    global timed, chatPos
    data = str(request.GET['data'])
    data = json.loads(data)
    timed   = data['timed'  ]
    chatPos = data['chatPos']
    return HttpResponse('all is well')
   
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

def Search(request):
    tag = int(request.GET['id'])
    post = Post.objects.filter(id = tag)[0]
    if post.isQues == True:
        b = {}
        b['id'       ] = str(post.id)
        b['message'  ] = str(post.message)
        b['fromUser' ] = str(post.fromUser)
        b['timestamp'] = str(post.timestamp)
        b['isQues'   ] = True
        b['isAns'    ] = False
        b['hasAns'   ] = False
        a = []
        for j in post.comment_set.all():
            c={}
            b['hasAns'   ] = True
            c['id'       ] = str(j.post.id)
            c['message'  ] = str(j.message)
            c['timestamp'] = str(j.timestamp)
            c['fromUser' ] = str(j.fromUser)
            c['isQues'   ] = False
            c['isAns'    ] = True
            a.append(c)
        data = {'ques':b,'answer':a}
    else :
        data = {'ques':{},'answer':[]}
    data = json.dumps(data)
    return HttpResponse(data)

def Delete (request):
    delId = int(request.GET['id'])
    Post.objects.filter(id=delId).delete()
    return HttpResponse('deleted')

def ComDelete (request):
    delId = int(request.GET['id'])
    Comment.objects.filter(id=delId).delete()
    return HttpResponse('deleted')

def GetInsertQuery (request):
    s = ''
    # state can be either threaded or timed..
    state = str (request.GET['state'])

    if state == 'Threaded':
        a = []
        for i in Post.objects.all():
            if i.isQues == True:
                b = {}
                b['id'       ] = str(i.id)
                b['message'  ] = str(i.message)
                b['fromUser' ] = str(i.fromUser)
                b['timestamp'] = str(i.timestamp)
                b['isQues'   ] = True
                b['isAns'    ] = False
                b['hasAns'   ] = False
                b['ans'      ] = []
#               s += 'Q' + str(i.id) + ' ' + str(i.fromUser) + ':\n' + str(i.message) + '\n'
                for j in i.comment_set.all():
                    c={}
                    b['hasAns'   ] = True
                    c['id'       ] = str(j.post.id)
                    c['myId'     ] = j.id
                    c['message'  ] = str(j.message)
                    c['timestamp'] = str(j.timestamp)
                    c['fromUser' ] = str(j.fromUser)
                    c['isQues'   ] = False
                    c['isAns'    ] = True
                    b['ans'      ].append(c)
                a.append(b)
#                   s += 'A' + str(i.id) + ' ' + str(j.fromUser) + ':\n' + str(j.message) + '\n'
    elif state == 'Timed':
        a = []
        for i in Post.objects.all():
            b = {}
            b['id'       ] = i.id
            b['message'  ] = i.message
            b['fromUser' ] = i.fromUser
            b['timestamp'] = str(i.timestamp)
            b['isQues'   ] = i.isQues
            b['isAns'    ] = False
            b['hasAns']    = False
            b['ans']       = []
            for j in i.comment_set.all():
                b['hasAns'] = True
                c = {}
                c['id'] =str(j.post.id)
                c['message'] = str(j.message)
                c['fromUser'] = str(j.fromUser)
                b['ans'].append(c)
            a.append(b)
        for i in Comment.objects.all():
            b={}
            b['id'       ] = i.post.id
            b['postMessage'] = i.post.message
            b['myId'     ] = i.id
            b['message'  ] = i.message
            b['timestamp'] = str(i.timestamp)
            b['fromUser' ] = i.fromUser
            b['isQues'   ] = False
            b['isAns'    ] = True
            a.append(b)
        # Sort the combined list using the key 'timestamp'
        a = sorted (a, key=itemgetter('timestamp'))
#       s = ''
#       for i in sortedList:
#           if i['isQues'] == True:
#               s += 'Q' + str(i['id']) + ' ' + str(i['fromUser']) + ':\n' + str(i['message']) + '\n'
#           elif i['isQues'] is False and i.has_key('isAns') and i['isAns'] is True:
#               s += 'A' + str(i['id']) + ' ' + str(i['fromUser']) + ':\n' + str(i['message']) + '\n'
#           else:
#               s += str(i['fromUser']) + ':\n' + str(i['message']) + '\n'
    data = json.dumps(a)
    return HttpResponse(data)

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
    password = str(request.GET['pass'    ])
    user = authenticate (username=username, password=password)
    if user is not None:
        login (request, user)
        TA = Group.objects.filter(name='TA')[0]
        if user in TA.user_set.all():
            data = {'uname':username,'isTA':True}
        else:
            data = {'uname':username,'isTA':False}
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


def GetLoggedinUsers (request):
    s = Session.objects.filter (expire_date__gte=timezone.now())
    uid = []
    for i in s:
        uid.append(i.get_decoded().get('_auth_user_id', None))
    a = Group.objects.filter(name='TA')[0].user_set.all().filter(id__in=uid)
    b = Group.objects.filter(name='Student')[0].user_set.all().filter(id__in=uid)
    t = [i.username for i in a]
    s = [i.username for i in b]
    ret = {'ta':t, 'student':s}
    return HttpResponse (json.dumps(ret))

def GetAllUsers (request):
    TA      = Group.objects.filter(name='TA')[0]
    Student = Group.objects.filter(name='Student')[0]
    t = [ta.username for ta in TA.user_set.all()]
    s = [st.username for st in Student.user_set.all()]
    ret = {'ta':t, 'student':s}
    return HttpResponse (json.dumps(ret))

