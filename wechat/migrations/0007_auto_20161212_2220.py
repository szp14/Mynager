# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2016-12-12 14:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0006_remove_meeting_homepage_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='idcard_image',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='myuser',
            name='user_image',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
    ]
