# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import ensomus.models


class Migration(migrations.Migration):

    dependencies = [
        ('ensomus', '0005_auto_20160831_1637'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('title', models.TextField(null=True, verbose_name='text')),
                ('is_achieved', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(related_name='goal_created_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='created by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('updated_by', models.ForeignKey(related_name='goal_updated_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'goal',
                'verbose_name_plural': 'goals',
            },
        ),
        migrations.CreateModel(
            name='GoalAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('title', models.TextField(null=True, verbose_name='text')),
                ('file', models.FileField(upload_to=ensomus.models.answer_file_dir_path, storage=ensomus.models.OverwriteStorage(), verbose_name='answer_file', blank=True)),
                ('created_by', models.ForeignKey(related_name='goalanswer_created_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='created by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('goal', models.ForeignKey(related_name='goal_answers', verbose_name='goal', to='ensomus.Goal')),
                ('updated_by', models.ForeignKey(related_name='goalanswer_updated_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'goal answer',
                'verbose_name_plural': 'goal answers',
            },
        ),
        migrations.RemoveField(
            model_name='answer',
            name='file',
        ),
        migrations.RemoveField(
            model_name='question',
            name='is_achieved',
        ),
    ]
