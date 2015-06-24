# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20150619_1911'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=128)),
                ('name', models.CharField(max_length=100, verbose_name=b'Full Name')),
                ('email', models.CharField(max_length=100, verbose_name=b'email id')),
            ],
        ),
        migrations.AlterField(
            model_name='comment',
            name='fromUser',
            field=models.ForeignKey(to='polls.User'),
        ),
        migrations.AlterField(
            model_name='post',
            name='fromUser',
            field=models.ForeignKey(to='polls.User'),
        ),
    ]
