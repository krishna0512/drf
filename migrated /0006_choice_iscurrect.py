# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20150630_0240'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='isCurrect',
            field=models.BooleanField(default=False),
        ),
    ]
