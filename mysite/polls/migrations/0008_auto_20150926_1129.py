# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='correct',
            field=models.CharField(default='', max_length=20000, verbose_name=b'list of users given correct answers.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='incorrect',
            field=models.CharField(default='', max_length=20000, verbose_name=b'list of users given incorrect ans...'),
            preserve_default=False,
        ),
    ]
