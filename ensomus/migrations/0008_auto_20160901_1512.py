# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ensomus', '0007_auto_20160901_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='slider',
            field=models.ForeignKey(related_name='sliders', default=1, verbose_name='slider', to='ensomus.Slider'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='slider',
            name='competence_part',
            field=models.ForeignKey(verbose_name='competence part', blank=True, to='ensomus.CompetencePart', null=True),
        ),
    ]
