# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import filebrowser_safe.fields
from django.conf import settings
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20150527_1555'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pages.Page')),
                ('full_text', mezzanine.core.fields.RichTextField(default=b'', help_text='The full activity text', verbose_name='full text', blank=True)),
                ('goals', mezzanine.core.fields.RichTextField(default=b'', help_text='What are the overall aims of the activity.', verbose_name='goals', blank=True)),
                ('summary', mezzanine.core.fields.RichTextField(default=b'', help_text='A catchy introductory paragraph.', verbose_name='summary', blank=True)),
                ('observing_time', models.IntegerField(null=True, verbose_name='Observing time', blank=True)),
                ('archive_data', models.BooleanField(default=False, verbose_name='Archive data')),
                ('planning', mezzanine.core.fields.RichTextField(default=b'', help_text='What do you need to do in preparation.', verbose_name='planning', blank=True)),
                ('background', mezzanine.core.fields.RichTextField(default=b'', help_text='What background information would useful to a non-specialist.', verbose_name='background', blank=True)),
                ('next_steps', mezzanine.core.fields.RichTextField(default=b'', help_text='What can the audience do after this activity?', verbose_name='next steps', blank=True)),
                ('featured_image', filebrowser_safe.fields.FileBrowseField(max_length=200, null=True, verbose_name=b'Image', blank=True)),
                ('related_posts', models.ManyToManyField(related_name='related_posts_rel_+', verbose_name='Related activities', to='lcogt.Activity', blank=True)),
                ('user', models.ForeignKey(related_name='activitys', verbose_name='Author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('_order',),
                'db_table': 'lcogt_activity',
            },
            bases=('pages.page', models.Model),
        ),
        migrations.CreateModel(
            name='LCOPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pages.Page')),
                ('content', mezzanine.core.fields.RichTextField(default=b'', help_text='Main content', verbose_name='Content', blank=True)),
                ('extra_info', mezzanine.core.fields.RichTextField(default=b'', help_text='This information will appear in the side bar', verbose_name='extra information', blank=True)),
                ('no_side_block', models.BooleanField(default=False, help_text="Check this if you don't want a side block", verbose_name='No side block')),
            ],
            options={
                'ordering': ('_order',),
                'db_table': 'lcogt_lcopage',
                'verbose_name': 'Page+',
                'verbose_name_plural': 'Pages+',
            },
            bases=('pages.page',),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mugshot', filebrowser_safe.fields.FileBrowseField(max_length=200, null=True, verbose_name='Mugshot', blank=True)),
                ('bio', mezzanine.core.fields.RichTextField(default=b'', help_text='This field can contain HTML and should contain a few paragraphs describing the background of the person.', verbose_name='biography', blank=True)),
                ('job_title', models.CharField(help_text='Example: Observatory Director', max_length=60, verbose_name='job title', blank=True)),
                ('research_interests', models.CharField(help_text='Comma separated list', max_length=255, verbose_name='research interests', blank=True)),
                ('current', models.BooleanField(default=True, verbose_name='current staff')),
                ('science_team', models.BooleanField(default=False, verbose_name='member of the science team')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'lcogt_profile',
                'verbose_name': 'LCOGT Person',
                'verbose_name_plural': 'LCOGT People',
            },
        ),
        migrations.CreateModel(
            name='Seminar',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pages.Page')),
                ('abstract', mezzanine.core.fields.RichTextField(default=b'', help_text='What the talk will be about.', verbose_name='abstract', blank=True)),
                ('seminardate', models.DateTimeField(default=datetime.datetime(2016, 1, 8, 11, 48, 37, 449232), verbose_name='Seminar date/time')),
                ('speaker_name', models.CharField(max_length=255, null=True, blank=True)),
                ('speaker_institute', models.CharField(max_length=255, null=True, blank=True)),
                ('speaker_picture', filebrowser_safe.fields.FileBrowseField(max_length=200, null=True, verbose_name='Speaker mugshot', blank=True)),
                ('speaker_biog', mezzanine.core.fields.RichTextField(default=b'', help_text='This field can contain HTML and should contain a few paragraphs describing the background of the person.', verbose_name='biography', blank=True)),
                ('speaker_link', models.URLField(help_text="Link to speaker's institutional page.")),
            ],
            options={
                'ordering': ('_order',),
                'db_table': 'lcogt_seminar',
            },
            bases=('pages.page',),
        ),
    ]
