# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20150709_1147'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=200, verbose_name=b'name of user')),
                ('isCorrect', models.BooleanField(default=False, verbose_name=b'is Correct')),
                ('ques', models.ForeignKey(to='polls.Question')),
            ],
        ),
    ]
