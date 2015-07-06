# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20150622_1854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='fromUser',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='post',
            name='fromUser',
            field=models.CharField(max_length=200),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
