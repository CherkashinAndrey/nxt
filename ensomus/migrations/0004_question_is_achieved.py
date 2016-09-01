# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ensomus', '0003_auto_20160830_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='is_achieved',
            field=models.BooleanField(default=False),
        ),
    ]
