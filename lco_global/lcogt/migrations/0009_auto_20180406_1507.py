# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-04-06 15:07
from __future__ import unicode_literals

from django.db import migrations
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('lcogt', '0008_auto_20180405_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='suitability',
            field=mezzanine.core.fields.MultiChoiceField(choices=[(b'6', b'6-11'), (b'11', b'11-16'), (b'16', b'16-18'), (b'all', b'All')], default=b'all', help_text='What can the audience do after this activity?', max_length=3),
        ),
    ]
