# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('ensomus', '0008_auto_20160901_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='slider',
            name='created_at',
            field=models.DateTimeField(verbose_name='created at', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='slider',
            name='created_by',
            field=models.ForeignKey(related_name='slider_created_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='created by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='slider',
            name='updated_at',
            field=models.DateTimeField(verbose_name='updated at', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='slider',
            name='updated_by',
            field=models.ForeignKey(related_name='slider_updated_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
