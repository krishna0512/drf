from django.db import models

# Create your models here.
class Post (models.Model):
	message = models.CharField (max_length=20000)
	timestamp = models.DateTimeField ('Time Published')
	fromUser = models.IntegerField (default=0)


class Comment (models.Model):
	post = models.ForeignKey (Post)
	message = models.CharField (max_length=20000)
	timestamp = models.DateTimeField ('Time Published')
	fromUser = models.IntegerField (default=0)
