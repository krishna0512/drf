# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20150706_1046'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('startedBy', models.CharField(max_length=200)),
                ('isActive', models.BooleanField(default=False)),
                ('isCompleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='session',
            name='startedBy',
        ),
        migrations.DeleteModel(
            name='Session',
        ),
    ]
