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



class Command(BaseCommand):
    """
    Implements a Drupal importer. Takes a file path or a URL for a JSON file
    from Drupal's Node Export i.e.
    ./drush node-export --type=book --format=json --file=book.json
    """

    option_list = BaseCommand.option_list + (
        make_option("-u", "--url", dest="url", help="URL to import file"),
    )

    help = 'Import JSON files containing Drupal Users'


    def handle(self, *args, **options):
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
        entries = json.load(jd)
        # Make a flat list of all the nodes which are parents to other nodes in Spacebook
        parents = set([e['book']['plid'] for e in entries if e['book']['bid']=='4012'])
        # Full list of nodes in SpaceBook
        sb_nodes = {e['book']['mlid']:e for e in entries if e['book']['bid']=='4012'}
        orphans = {}

        print "Read %s SpaceBook pages" % len(sb_nodes)
        # Create SpaceBook home first
        spacebook = sb_nodes['503']
        sb_page = make_page(spacebook)

        # Create parent pages first
        parents_lookup = {}
        for entry in parents:
            if entry != '0':
                new_page = make_page(sb_nodes[entry],sb_page)
                if new_page:
                    parents_lookup[entry] = new_page
                    print "Parents Created - %s" % new_page

        for key, entry in sb_nodes.items():
            direct_parent = near_parent(entry['book'],parents_lookup)
                
            # Get the time struct of the published date if possible and
            # the updated date if we can't.
            if key != '0':
                print "Creating %s" % key
                new_page = make_page(entry,direct_parent)
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

def set_keywords(page, disciplines):
    categories = {'6':'education','8':'science','5143':'observatory','9':'observatory','7':'observatory'}
    for disc in disciplines:
        try:
            kw = categories[disc['nid']]
            keyword_id = Keyword.objects.get_or_create(title=kw)[0].id
            page.keywords.add(AssignedKeyword(keyword_id=keyword_id))
        except Exception, e:
            print e
    keyword_id = Keyword.objects.get_or_create(title='spacebook')[0].id
    page.keywords.add(AssignedKeyword(keyword_id=keyword_id))
    return True


def make_page(entry,parent=None):
    cat_list = []
    pages = RichTextPage.objects.filter(title=entry['title'])
    if pages.count() == 0:
        rt = RichTextPage.objects.create(title=entry['title'], content=entry['body']['und'][0]['value'])
        pub_date = datetime.fromtimestamp(int(entry['created']))
        if entry['path']:
            rt.slug = entry['path']['alias']
        # rt.in_menus = []
        rt.publish_date = pub_date
        rt.parent = parent
        rt.save()
        if entry.get('field_discipline',False) and entry.get('field_discipline') != '':
            set_keywords(rt, entry['field_discipline']['und'])
        return rt
    else:
        return pages[0]

