# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ensomus', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='potenciale',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='potenciale', choices=[(b'YES', b'YES'), (b'NO', b'NO')]),
        ),
    ]
