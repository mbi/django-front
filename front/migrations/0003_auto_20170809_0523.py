# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-09 05:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0002_auto_20150123_0219'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='placeholderhistory',
            options={'ordering': ('-saved',)},
        ),
    ]
