# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-12 19:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20160512_1949'),
    ]

    operations = [
        migrations.AddField(
            model_name='mood',
            name='description',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
