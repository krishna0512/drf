# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='startedBy',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
