from django.core.management.base import CommandError, BaseCommand
from bs4 import BeautifulSoup
from mezzanine.pages.models import Page
from mezzanine.blog.models import BlogPost

from django.conf import settings
from lcogt.models import Activity, Seminar
from lcogt.admin import PageResource, SeminarResource, ActivityResource, PartnerResource, SpaceResource

import logging
import requests

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    Scan all or part of the website for dead links and images.
    """

    help = 'Export content following relationships'

    def handle(self, **options):

        contentpages = {
            'pages':PageResource,
            'seminars':SeminarResource,
            'partners':PartnerResource,
            'spacebook':SpaceResource,
            'activity':ActivityResource
        }
        for k,v in contentpages.items():
            dataset = v().export()
            with open('{}.json'.format(k),'w') as f:
                f.write(dataset.json)
