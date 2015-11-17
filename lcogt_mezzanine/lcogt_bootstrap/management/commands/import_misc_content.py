from __future__ import unicode_literals
from collections import defaultdict
from datetime import datetime, timedelta
from future.builtins import int
from lcogt.models import LCOPage
from mezzanine.pages.models import RichTextPage
from optparse import make_option
from time import mktime, timezone
from django.contrib.auth.models import User
import json
import re, pytz

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

        print "Read %s Pages" % len(entries)

        observatory,created = RichTextPage.objects.get_or_create(title='Observatory',slug='observatory',content='[Temp]')
        sites,created = RichTextPage.objects.get_or_create(title='Observatory Sites',slug='observatory/site',content='[Temp]', parent=observatory)
        telescopes,created = RichTextPage.objects.get_or_create(title='Telescopes',slug='observatory/telescope',content='[Temp]', parent=observatory)
        instruments,created = RichTextPage.objects.get_or_create(title='Instrumentation',slug='observatory/instruments',content='[Temp]', parent=observatory)

        parents = {'instrument':instruments,'instrument_inst':instruments,'spectrograph':instruments,'class':telescopes,'telescope_inst':telescopes, 'site': sites, 'page':None, 'article': None}
        # Create activities
        if created:
            print "Created Observatory page: %s" % observatory
        else:
            print "Found Observatory page: %s" % observatory
        for page in entries:
            if page['type'] in parents:
                new_page= make_page(page,media,parents[page['type']]) 


def add_attached_media(media, entry):
    image = ''
    if entry['field_media'] and entry['field_media'] != '':
        for line in entry['field_media']['und']:
            if not line.get('attributes',None):
                line['attributes'] ={'css_class' : 'side-image'}
            image += make_img_tag(media,line)
    return {'extra_info':image}

def make_page(entry,media,parent=None):
    status = {'0':1,'1':2}
    if LCOPage.objects.filter(title=entry['title']).count() == 0:
        initial = {
                'title'   : entry['title'],
                'content' : replace_media_tag(entry['body']['und'][0]['value'],media),
                'parent'  : parent,
                'status'  : status[entry['status']]
                 }
        pub_date = datetime.fromtimestamp(int(entry['created']))
        if entry['path']:
            initial['slug'] = entry['path']['alias']
        initial['publish_date'] = pub_date
        if entry.get('field_media',None):
            extras = add_attached_media(media, entry)
        else:
            extras = {}
        initial = dict(initial.items() + extras.items())
        page, created = LCOPage.objects.get_or_create(**initial)
        if entry.get('field_discipline',False) and entry.get('field_discipline') != '':
            set_keywords(page, entry['field_discipline']['und'])
        else:
            set_keywords(page,['9'])
        if created:
            print("Imported %s: %s" % (entry['type'],page))
        return page
    else:
        return LCOPage.objects.filter(title=entry['title'])[0], None

