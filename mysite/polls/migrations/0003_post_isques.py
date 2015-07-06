# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_remove_post_isques'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='isQues',
            field=models.BooleanField(default=False, verbose_name=b'Is Question'),
        ),
    ]
