from django.core.management.base import CommandError, BaseCommand
from mezzanine.pages.models import RichTextPage
from lcogt.models import SpacePage

import logging
import requests
from datetime import datetime

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    Convert all SpaceBook pages to custom content type
    """

    help = 'Convert all SpaceBook pages to custom content type'

    def add_arguments(self, parser):
        parser.add_argument("-d", "--dry-run", dest='dryrun', action='store_true', help="dry run, no DB commits")


    def handle(self, **options):
        parents = RichTextPage.objects.filter(keywords_string__contains='spacebook', parent_id = 2)
        now = datetime.utcnow()
        for page in spacepages:
            self.make_page(page)


    def make_page(page):
        spacepage = SpacePage.objects.get_or_create(title=page.title)
        spacepage.content = page.content
        spacepage.publish_date = now
        spacepage.slug = page.slug

        page.status = 1
        page.save()
        return spacepage
