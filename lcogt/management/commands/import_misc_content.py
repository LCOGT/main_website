from __future__ import unicode_literals
from collections import defaultdict
from datetime import datetime, timedelta
from future.builtins import int
from mezzanine.pages.models import Page, RichTextPage
from lcogt.models import Activity
from optparse import make_option
from time import mktime, timezone
from django.contrib.auth.models import User
import json
import re

from django.core.management.base import CommandError, BaseCommand
from django.utils.html import linebreaks


class Command(BaseCommand):
    """
    Implements a Drupal importer. Takes a file path or a URL for a JSON file
    from Drupal's Node Export i.e.
    ./drush node-export --type=book --format=json --file=book.json
    """

    option_list = BaseCommand.option_list + (
        make_option("-u", "--url", dest="url", help="URL to import file"),
    )

    help = 'Import JSON file containing misc content'

    categories = {'6':'Education','8':'Science'}

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
            raise CommandError("You must provide a URL/file location for the data file")

        media = []
        # Read the JSON in from file
        jd = open(url)
        # Full list of Activity nodes 
        entries = json.load(jd)

        print "Read %s Pages" % len(entries)

        observatory,created = RichTextPage.objects.get_or_create(title='Observatory',slug='observatory',content='[Temp]', parent=observatory)
        sites,created = RichTextPage.objects.get_or_create(title='Observatory Sites',slug='observatory/site',content='[Temp]', parent=observatory)
        telescopes,created = RichTextPage.objects.get_or_create(title='Telescopes',slug='observatory/telescope',content='[Temp]', parent=observatory)
        instruments,created = RichTextPage.objects.get_or_create(title='Observatory Sites',slug='observatory/instruments',content='[Temp]', parent=observatory)
        # Create activities
        if created:
            print "Created Observatory page: %s" % observatory
        else:
            print "Found Observatory page: %s" % observatory
        for page in entries:
            if page['type'] in ['instrument_inst','article','spectrograph','site','class','telescope_inst']
            new_page, media_url = make_page(page,observatory)
            if media_url:
                media.append(media_url)
        if media:
            print "Update the media links for these pages:"
            for l in media:
                print l




def links_to_text(page_list, activities):
    html = "<ul>"
    for item in page_list:
        activity = activities[item]
        html += "<li><a href='%s'>%s</li>" % ()
    html += "</ul>"
    return html

def find_media_tag(content):
    x = re.findall('\[\[\{"type":"media"(.*\n?)\}\]\]', content, re.MULTILINE)
    if x:
        return x
    else:
        return None



def make_page(entry,parent):
    if Page.objects.filter(title=entry['title']).count() == 0:
        initial = {
                'title' :entry['title'],
                'content' :entry['body']['und'][0]['value'],
                'parent':parent}
        pub_date = datetime.fromtimestamp(int(entry['created']))
        if entry['path']:
            initial['slug'] = entry['path']['alias']
        initial['publish_date'] = pub_date
        page, created = RichTextPage.objects.get_or_create(**initial)
        media = find_media_tag(entry['body']['und'][0]['value'])
        if media:
            media_url = initial['slug']
        else:
            media_url = None
        return activity, media_url
    else:
        return Activity.objects.filter(title=entry['title'])[0], None

