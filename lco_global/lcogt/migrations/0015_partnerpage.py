# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-02-04 16:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import filebrowser_safe.fields
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_auto_20170411_0504'),
        ('lcogt', '0014_auto_20180601_1211'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartnerPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pages.Page')),
                ('organizers', models.CharField(blank=True, help_text='Example: Jane Doe', max_length=200, verbose_name='organizers names')),
                ('partner_logo', filebrowser_safe.fields.FileBrowseField(blank=True, max_length=200, null=True, verbose_name='parter logo')),
                ('organization', models.CharField(blank=True, help_text='Where is the project based, who is running it?', max_length=200, verbose_name='institution or organization')),
                ('outputs', mezzanine.core.fields.RichTextField(blank=True, default='', help_text='What did they achieve and want to share?', verbose_name='Outputs')),
                ('contact', models.CharField(blank=True, help_text='Link to contact page or email', max_length=200, verbose_name='contact')),
                ('active', models.BooleanField(default=True, verbose_name='active partner')),
                ('start', models.DateField(verbose_name='When did the partner start?')),
                ('end', models.DateField(blank=True, verbose_name='When did the partner project end?')),
            ],
            options={
                'verbose_name': 'Partner info page',
                'ordering': ('_order',),
            },
            bases=('pages.page',),
        ),
    ]
