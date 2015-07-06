from django.contrib import admin

from .models import *

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Question)
admin.site.register(Choice)
# Register your models here.
