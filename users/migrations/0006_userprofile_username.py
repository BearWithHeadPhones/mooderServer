# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-15 14:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_userprofile_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='username',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
