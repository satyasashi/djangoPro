# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-02-27 12:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='creted_on',
            new_name='created_on',
        ),
    ]
