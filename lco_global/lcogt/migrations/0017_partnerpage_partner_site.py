# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-02-04 16:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lcogt', '0016_partnerpage_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='partnerpage',
            name='partner_site',
            field=models.URLField(blank=True, verbose_name='Link to partner website'),
        ),
    ]
