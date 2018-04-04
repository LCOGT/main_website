import requests
from datetime import datetime
import pytz

from django.core.management.base import CommandError, BaseCommand
from django.db.models import Q

from mezzanine.pages.models import RichTextPage
from lcogt.models import SpacePage

class Command(BaseCommand):
    """
    Convert all SpaceBook pages to custom content type
    """

    help = 'Convert all SpaceBook pages to custom content type'

    def add_arguments(self, parser):
        parser.add_argument("-d", "--dry-run", dest='dryrun', action='store_true', help="dry run, no DB commits")


    def handle(self, **options):
        sb_home = RichTextPage.objects.get(keywords_string__contains='spacebook', title="Space Book")
        home_id = make_page(sb_home)
        home_map = {sb_home.id:home_id}

        pages = RichTextPage.objects.filter(keywords_string__contains='spacebook')
        parents = pages.filter(parent_id = 2)
        parent_ids = []
        parent_map = {} # {old:new}
        for parent in parents:
            parent_id = make_page(parent, home_map, True)
            parent_ids.append(parent_id)
            parent_map[parent.id] = parent_id
            print("{} parent created".format(parent.title))

        children = pages.filter(~Q(parent_id = 2))
        for child in children:
            page_id = make_page(child, parent_map)
            print("{} created".format(child.title))

        return

def make_page(page, parent_map=None, top_level=False):
    now = datetime.now(tz=pytz.utc)
    spacepage, created = SpacePage.objects.get_or_create(title=page.title)
    spacepage.content = page.content
    spacepage.publish_date = now
    spacepage.slug = page.slug
    if parent_map:
        try:
            parent_id = parent_map[page.parent_id]
        except:
            print("{} - incompatible Parent ID for {}".format(page.parent_id, page.title))
            return
        spacepage.parent_id = parent_id
        if top_level:
            titles = "SpaceBook / {}".format(page.title)
        else:
            spaceparent = SpacePage.objects.get(id=parent_id)
            titles = "SpaceBook / {} / {}".format(spaceparent.title, page.title)
    else:
        titles = "SpaceBook"
    spacepage.titles = titles
    spacepage.save()

    page.status = 1
    page.slug = "{}-old".format(page.slug)
    page.save()
    return spacepage.id
