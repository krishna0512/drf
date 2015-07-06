from django.db import models

# Create your models here.
class Post (models.Model):
    message = models.CharField ('Message', max_length=20000)
    timestamp = models.DateTimeField ('Time Published')
    fromUser = models.CharField ('From User', max_length=200)
    isQues = models.BooleanField('Is Question', default = False)

class Comment (models.Model):
    post = models.ForeignKey (Post)
    message = models.CharField ('Message', max_length=20000)
    timestamp = models.DateTimeField ('Time Published')
    fromUser = models.CharField ('From User', max_length=200)

class Question(models.Model):
    question_text = models.CharField('Question Text', max_length=20000)
    pub_date = models.DateTimeField('date/time published')


class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField('Choice Text', max_length=20000)
    isCurrect = models.BooleanField('is Correct', default = False)
    #votes = models.IntegerField(default=0)
