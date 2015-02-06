from __future__ import unicode_literals
from collections import defaultdict
from datetime import datetime, timedelta
from future.builtins import int
from mezzanine.pages.models import Page, RichTextPage
from mezzanine.generic.models import Keyword, AssignedKeyword
from optparse import make_option
from time import mktime, timezone
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
        entries = json.load(jd)
        # Make a flat list of all the nodes which are parents to other nodes in Spacebook
        parents = set([e['book']['plid'] for e in entries if e['book']['bid']=='4012'])
        # Full list of nodes in SpaceBook
        sb_nodes = {e['book']['mlid']:e for e in entries if e['book']['bid']=='4012'}
        orphans = {}

        print "Read %s SpaceBook pages" % len(sb_nodes)
        # Create SpaceBook home first
        spacebook = sb_nodes['503']
        sb_page = make_page(spacebook,media)

        # Create parent pages first
        parents_lookup = {}
        for entry in parents:
            if entry != '0' and entry !='503':
                new_page = make_page(sb_nodes[entry],media,sb_page)
                if new_page:
                    parents_lookup[entry] = new_page
                    print "Parents Created - %s" % new_page

        for key, entry in sb_nodes.items():
            direct_parent = near_parent(entry['book'],parents_lookup)
                
            # Get the time struct of the published date if possible and
            # the updated date if we can't.
            if key != '0' and key !='503' and key not in parents:
                print "Creating %s" % key
                new_page = make_page(entry,media,direct_parent)
                if new_page:
                    print "Pages Created - %s" % new_page
                    if not direct_parent:
                        orphans[key] = new_page

        # Find parents for orphaned pages
        for key, orphan in orphans.items():
            direct_parent = near_parent(entry['book'],parents_lookup)
            if direct_parent:
                orphan.parent = direct_parent
                orphan.save()


def near_parent(book,parents_lookup):
    parent = book['plid']
    nearest_parent = parents_lookup.get(parent,None)
    return nearest_parent


def make_page(entry,media,parent=None):
    status = {'0':1,'1':2}
    cat_list = []
    pages = RichTextPage.objects.filter(title=entry['title'])
    if pages.count() == 0:
        rt = RichTextPage.objects.create(title=entry['title'])
        content = replace_media_tag(entry['body']['und'][0]['value'],media)
        rt.content = content
        pub_date = datetime.fromtimestamp(int(entry['created']))
        rt.status = status[entry['status']]
        if entry['path']:
            rt.slug = entry['path']['alias']
        # rt.in_menus = []
        rt.publish_date = pub_date
        rt.parent = parent
        rt.save()
        if entry.get('field_discipline',False) and entry.get('field_discipline') != '':
            set_keywords(rt, entry['field_discipline']['und'],True)
        return rt
    else:
        return pages[0]

