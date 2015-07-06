# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('choice_text', models.CharField(max_length=20000, verbose_name=b'Choice Text')),
                ('isCurrect', models.BooleanField(default=False, verbose_name=b'is Correct')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.CharField(max_length=20000, verbose_name=b'Message')),
                ('timestamp', models.DateTimeField(verbose_name=b'Time Published')),
                ('fromUser', models.CharField(max_length=200, verbose_name=b'From User')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.CharField(max_length=20000, verbose_name=b'Message')),
                ('timestamp', models.DateTimeField(verbose_name=b'Time Published')),
                ('fromUser', models.CharField(max_length=200, verbose_name=b'From User')),
                ('isQues', models.BooleanField(default=False, verbose_name=b'Is Question')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_text', models.CharField(max_length=20000, verbose_name=b'Question Text')),
                ('pub_date', models.DateTimeField(verbose_name=b'date/time published')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(to='polls.Post'),
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(to='polls.Question'),
        ),
    ]
