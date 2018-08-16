# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-06-01 12:11
from __future__ import unicode_literals

from django.db import migrations, models
import filebrowser_safe.fields
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('lcogt', '0013_auto_20180511_0830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='agerange',
            field=mezzanine.core.fields.MultiChoiceField(choices=[('7', '7-11'), ('11', '11-16'), ('16', '16+')], default='all', help_text='What is the age range for this activity?', max_length=20),
        ),
        migrations.AlterField(
            model_name='activity',
            name='background',
            field=mezzanine.core.fields.RichTextField(blank=True, default='', help_text='What background information would useful to a non-specialist.', verbose_name='background'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='evaluation',
            field=mezzanine.core.fields.RichTextField(blank=True, default='', help_text='How to ensure the goals are reached', verbose_name='evaluation'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='featured_image',
            field=filebrowser_safe.fields.FileBrowseField(blank=True, max_length=200, null=True, verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='full_text',
            field=mezzanine.core.fields.RichTextField(blank=True, default='', help_text='The full activity text', verbose_name='full text'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='goals',
            field=mezzanine.core.fields.RichTextField(blank=True, default='', help_text='What are the overall aims of the activity.', verbose_name='goals'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='next_steps',
            field=mezzanine.core.fields.RichTextField(blank=True, default='', help_text='What can the audience do after this activity?', verbose_name='next steps'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='planning',
            field=mezzanine.core.fields.RichTextField(blank=True, default='', help_text='What do you need to do in preparation.', verbose_name='planning'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='summary',
            field=mezzanine.core.fields.RichTextField(blank=True, default='', help_text='A catchy introductory paragraph.', verbose_name='summary'),
        ),
        migrations.AlterField(
            model_name='lcopage',
            name='content',
            field=mezzanine.core.fields.RichTextField(blank=True, default='', help_text='Main content', verbose_name='Main Content'),
        ),
        migrations.AlterField(
            model_name='lcopage',
            name='extra_info',
            field=mezzanine.core.fields.RichTextField(blank=True, default='', help_text='This information will appear in the side bar or directly below title if No Side Block is checked', verbose_name='Extra info'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=mezzanine.core.fields.RichTextField(blank=True, default='', help_text='This field can contain HTML and should contain a few paragraphs describing the background of the person.', verbose_name='biography'),
        ),
        migrations.AlterField(
            model_name='seminar',
            name='abstract',
            field=mezzanine.core.fields.RichTextField(blank=True, default='', help_text='What the talk will be about.', verbose_name='abstract'),
        ),
        migrations.AlterField(
            model_name='seminar',
            name='speaker_biog',
            field=mezzanine.core.fields.RichTextField(blank=True, default='', help_text='This field can contain HTML and should contain a few paragraphs describing the background of the person.', verbose_name='biography'),
        ),
        migrations.AlterField(
            model_name='seminar',
            name='speaker_name',
            field=models.CharField(default='tdb', max_length=255),
        ),
        migrations.AlterField(
            model_name='spacepage',
            name='content',
            field=mezzanine.core.fields.RichTextField(blank=True, default='', help_text='page text', verbose_name='content'),
        ),
    ]