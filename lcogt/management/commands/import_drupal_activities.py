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

    help = 'Import JSON file containing Activities'

    categories = {'6':'education','8':'science','5143':'observatory','9':'observatory','7':'observatory'}

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
        activities = {e['nid']:e for e in entries}

        print "Read %s Activities" % len(entries)

        education,created = RichTextPage.objects.get_or_create(title='Education',slug='education',content='[Temp]')
        activity_page, created = RichTextPage.objects.get_or_create(title="Activities",slug='education/activities',content='[Temp]',parent=education)
        # Create activities
        if created:
            print "Created Education and Activities page: %s" % activity_page
        else:
            print "Found Education and Activities page: %s" % activity_page
        for k, page in activities.items():
            new_a, media_url = make_activity(page,activity_page)
            activities[k]['new_activity'] = new_a
            if media_url:
                media.append(media_url)
        if media:
            print "Update the media links for these pages:"
            for l in media:
                print l
        # Add extra data fields
        for k, page in activities.items():
            # Add building blocks:
            for field_name in ['field_building_blocks','field_next_steps', 'field_based_on']:
                if page[field_name]:
                    for nid in page[field_name]['und']:
                        activity = activities.get(nid['nid'],None)
                        if activity:
                            page['new_activity'].related_posts.add(activity['new_activity'])




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

def set_keywords(disciplines):
    keywords = []
    for disc in disciplines:
        try:
            kw = categories[disc['nid']]
            keywords.append(kw)
        except:
            pass
    return keywords


def make_activity(entry,parent):
    if Activity.objects.filter(title=entry['title']).count() == 0:
        initial = {
                'title' :entry['title'],
                'full_text' :entry['body']['und'][0]['value'],
                'parent':parent}
        pub_date = datetime.fromtimestamp(int(entry['created']))
        try:
            email = "%s@lcogt.net" % entry['name']
            mezzanine_user = User.objects.get(email=email)
        except User.DoesNotExist:
            mezzanine_user = User.objects.get(pk=1)
        initial['user'] = mezzanine_user
        if entry['path']:
            initial['slug'] = entry['path']['alias']
        if entry['field_goals']:
            initial['goals'] = entry['field_goals']['und'][0]['value']
        if entry['field_planning']:
            initial['planning'] = entry['field_planning']['und'][0]['value']
        # if entry['field_archive']:
        #      initial.archive = {u'und': [{u'value': u'no-archive'}]]
        if entry['field_objectives']:
            initial['summary'] = entry['field_objectives']['und'][0]['value']
        if entry['field_observing_time']:
            initial['observing_time'] = int(entry['field_observing_time']['und'][0]['value'])
        initial['publish_date'] = pub_date
        if entry.get('field_discipline',None):
            set_keywords(page, entry['field_discipline']['und'])
        activity, created = Activity.objects.get_or_create(**initial)
        media = find_media_tag(entry['body']['und'][0]['value'])
        if media:
            media_url = initial['slug']
        else:
            media_url = None
        return activity, media_url
    else:
        return Activity.objects.filter(title=entry['title'])[0], None

