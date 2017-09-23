# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placeholderhistory',
            name='placeholder',
            field=models.ForeignKey(related_name='history', to='front.Placeholder', on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
