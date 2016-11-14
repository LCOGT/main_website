# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-29 14:15
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('lcogt', '0004_auto_20160811_2345'),
    ]

    operations = [
        migrations.AddField(
            model_name='lcopage',
            name='use_parent',
            field=models.BooleanField(default=False, help_text='Check if you want to use a longer title and have it appear below the bar', verbose_name="Use parent's title"),
        ),
        migrations.AlterField(
            model_name='lcopage',
            name='content',
            field=mezzanine.core.fields.RichTextField(blank=True, default=b'', help_text='Main content', verbose_name='Main Content'),
        ),
        migrations.AlterField(
            model_name='lcopage',
            name='extra_info',
            field=mezzanine.core.fields.RichTextField(blank=True, default=b'', help_text='This information will appear in the side bar or directly below title if No Side Block is checked', verbose_name='Extra info'),
        ),
    ]