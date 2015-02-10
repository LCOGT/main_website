from __future__ import unicode_literals
from collections import defaultdict
from datetime import datetime, timedelta
from future.builtins import int
from mezzanine.pages.models import Page, RichTextPage
from lcogt.models import Seminar
from optparse import make_option
from time import mktime, timezone
from django.contrib.auth.models import User
import json
import re

from django.core.management.base import CommandError, BaseCommand
from django.utils.html import linebreaks

from lcogt.utils import *

class Command(BaseCommand):
    """
    Implements a Drupal importer. Takes a file path or a URL for a JSON file
    from Drupal's Node Export i.e.
    ./drush node-export --type=book --format=json --file=book.json
    """

    option_list = BaseCommand.option_list + (
        make_option("-u", "--url", dest="url", help="URL to import file"),
        make_option("-d", "--dbname", dest="dbname", help="Name of the Drupal DB name"),
        make_option("-i", "--user", dest="user", help="Username for the Drupal DB"),
        make_option("-p", "--password", dest="password", help="Password for the Drupal DB"),
        make_option("-n", "--host", dest="host", help="Host for the Drupal DB"),
    )

    help = 'Import JSON file containing misc content'

    def handle(self, **options):
        """
        Gets the posts from either the provided URL or the path if it
        is local.

        Fields to keep:
        - title
        - body
        - Discipline => category
        - Attached image/media file
        - Author
        - Publication date
        - Published/not published
        """
        try:
            url = options.get("url")
        except:
            raise CommandError("You must provide a URL/file location for the data file.")
        try:
            dbname = options.get("dbname")
        except:
            raise CommandError("You must provide the database name")
        try:
            user = options.get("user")
        except:
            raise CommandError("You must provide the database user name")
        try:
            password = options.get("password")
        except:
            raise CommandError("You must provide the database password")
        try:
            host = options.get("host")
        except:
            raise CommandError("You must provide the database hostname")

        #find media files from Drupal DB
        media = get_media(dbname,user,password,host)
        # Read the JSON in from file
        jd = open(url)
        # Full list of Activity nodes 
        entries = json.load(jd)

        print "Read %s Activities" % len(entries)

        science_page,created = RichTextPage.objects.get_or_create(title='Science',slug='science',content='[Temp]')
        seminar_page,created = RichTextPage.objects.get_or_create(title='Science Seminars',slug='seminar',content='[Temp]',parent=science_page)
        # Create activities
        if created:
            print "Created Science page: %s" % seminar_page
        else:
            print "Found Science page: %s" % seminar_page
        for page in entries:
            new_a = make_seminar(page,media,seminar_page)


def make_seminar(entry,media,parent):
    status = {'0':1,'1':2}
    if Seminar.objects.filter(title=entry['title']).count() == 0:
        initial = {
                'title' :entry['title'],
                'parent':parent}
        pub_date = datetime.fromtimestamp(int(entry['created']))
        content = replace_media_tag(entry['body']['und'][0]['value'],media)
        initial['abstract'] = content
        initial['status'] = status[entry['status']]

        if entry['path']:
            initial['slug'] = entry['path']['alias']
        if entry['field_seminardate']:
            initial['seminardate'] = datetime.strptime(entry['field_seminardate']['und'][0]['value'], "%Y-%m-%dT%H:%M:%S")
        if entry['field_speaker']:
            initial['speaker_name'] = entry['field_speaker']['und'][0]['value']
        if entry['field_place']:
            initial['speaker_institute'] = entry['field_place']['und'][0]['value']
        if entry['field_about_me']:
            initial['speaker_biog'] = entry['field_about_me']['und'][0]['value']
        if entry['field_link']:
            initial['speaker_link'] = entry['field_link']['und'][0]['value']
        if entry['field_profile']:
            fid = entry['field_profile']['und'][0]['fid']
            filename = media.get(fid,None)
            initial['speaker_picture'] = filename
        seminar, created = Seminar.objects.get_or_create(**initial)
        if entry.get('field_discipline',None):
            set_keywords(seminar, [{'nid':'8'}])
        if created:
            print("Imported Seminar: %s" % seminar)
        return seminar
    else:
        return Seminar.objects.filter(title=entry['title'])[0], None

