# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-08-12 08:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postapp', '0002_post_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='uid',
            field=models.IntegerField(),
        ),
    ]