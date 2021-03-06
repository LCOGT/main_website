# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-04-05 12:53
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('lcogt', '0007_spacepage'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='evaluation',
            field=mezzanine.core.fields.RichTextField(blank=True, default=b'', help_text='How to ensure the goals are reached', verbose_name='evaluation'),
        ),
        migrations.AddField(
            model_name='activity',
            name='suitability',
            field=models.IntegerField(choices=[(1, b'6-11'), (2, b'12-16'), (3, b'16-18'), (4, b'All')], default=4, help_text='What can the audience do after this activity?'),
        ),
    ]
