# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ensomus.models


class Migration(migrations.Migration):

    dependencies = [
        ('ensomus', '0004_question_is_achieved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='competence',
            name='company',
        ),
        migrations.RemoveField(
            model_name='competence',
            name='is_manager',
        ),
        migrations.AddField(
            model_name='answer',
            name='file',
            field=models.FileField(upload_to=ensomus.models.answer_file_dir_path, storage=ensomus.models.OverwriteStorage(), verbose_name='answer_file', blank=True),
        ),
    ]
