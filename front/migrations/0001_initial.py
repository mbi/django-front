# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Placeholder',
            fields=[
                ('key', models.CharField(max_length=40, serialize=False, primary_key=True, db_index=True)),
                ('value', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlaceholderHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.TextField(blank=True)),
                ('saved', models.DateTimeField(auto_now_add=True)),
                ('placeholder', models.ForeignKey(to='front.Placeholder', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': (b'-saved',),
            },
            bases=(models.Model,),
        ),
    ]
