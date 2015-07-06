# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import polls.models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_choice_iscurrect'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='isQues',
            field=models.BooleanField(default=False, verbose_name=b'Is Question'),
        ),
        migrations.AlterField(
            model_name='choice',
            name='choice_text',
            field=models.CharField(max_length=20000, verbose_name=b'Choice Text'),
        ),
        migrations.AlterField(
            model_name='choice',
            name='isCurrect',
            field=models.BooleanField(default=False, verbose_name=b'is Correct'),
        ),
        migrations.AlterField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(to='polls.Question', to_field=polls.models.Question),
        ),
        migrations.AlterField(
            model_name='comment',
            name='fromUser',
            field=models.CharField(max_length=200, verbose_name=b'From User'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='message',
            field=models.CharField(max_length=20000, verbose_name=b'Message'),
        ),
        migrations.AlterField(
            model_name='post',
            name='fromUser',
            field=models.CharField(max_length=200, verbose_name=b'From User'),
        ),
        migrations.AlterField(
            model_name='post',
            name='message',
            field=models.CharField(max_length=20000, verbose_name=b'Message'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.CharField(max_length=20000, verbose_name=b'Question Text'),
        ),
    ]
