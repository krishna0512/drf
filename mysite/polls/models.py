from django.db import models

# Create your models here.
class Post (models.Model):
	message = models.CharField (max_length=20000)
	timestamp = models.DateTimeField ('Time Published')
	fromUser = models.CharField (max_length=200)


class Comment (models.Model):
	post = models.ForeignKey (Post)
	message = models.CharField (max_length=20000)
	timestamp = models.DateTimeField ('Time Published')
	fromUser = models.CharField (max_length=200)

class Question(models.Model):
    question_text = models.CharField(max_length=20000)
    pub_date = models.DateTimeField('date/time published')


class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=20000)
    #votes = models.IntegerField(default=0)

