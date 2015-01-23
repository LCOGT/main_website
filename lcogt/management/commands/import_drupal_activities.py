from __future__ import unicode_literals
from collections import defaultdict
from datetime import datetime, timedelta
from future.builtins import int
from mezzanine.pages.models import Page, RichTextPage
from lcogt.models import Activity
from optparse import make_option
from time import mktime, timezone
import json
import re

from django.core.management.base import CommandError, BaseCommand
from django.utils.html import linebreaks

from mezzanine.blog.management.base import BaseImporterCommand


class Command(BaseImporterCommand):
    """
    Implements a Drupal importer. Takes a file path or a URL for a JSON file
    from Drupal's Node Export i.e.
    ./drush node-export --type=book --format=json --file=book.json
    """

    option_list = BaseImporterCommand.option_list + (
        make_option("-u", "--url", dest="url", help="URL to import file"),
    )

    help = 'Import JSON file containing Activities'

    categories = {'6':'Education','8':'Science'}

    def handle_import(self, options):
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

        url = options.get("url")
        if url is None:
            raise CommandError("Usage is import_drupal_spacebook %s" % self.args)

        # Read the JSON in from file
        jd = open(url)
        # Full list of Activity nodes 
        entries = json.load(jd)
        activities = {e['nid']:e for e in entries}

        print "Read %s Activities" % len(entries)
        for k, page in entries.items():
            make_page(page)



def find_author(username):
    user

def make_page(entry):
    cat_list = []
    if RichTextPage.objects.filter(title=entry['title']).count() == 0:
        rt = Activity.objects.create(title=entry['title'], content=entry['body']['und'][0]['value'])
        pub_date = datetime.fromtimestamp(int(entry['created']))
        if entry['path']:
            rt.slug = entry['path']['alias']
        rt.in_menus = []
        for item in getattr(entry['field_discipline'], "und", []):
            cat = categories.getattr(item,None)
            if cat:
                cat_list.append(cat)
        rt.publish_date = pub_date
        rt.keywords = ",".join(cat_list)
        rt.parent = parent
        rt.save()
        return rt
    else:
        return None

