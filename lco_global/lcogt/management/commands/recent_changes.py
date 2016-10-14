from django.core.management.base import CommandError, BaseCommand
from mezzanine.pages.models import Page
from mezzanine.blog.models import BlogPost
from lcogt.models import Activity, Seminar
from datetime import datetime, timedelta

import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    Scan all or part of the website for dead links and images.
    """

    help = 'Scan all or part of the website for dead links and images'

    def add_arguments(self, parser):
        parser.add_argument("-f", "--full", dest='full', action='store_true', help="full website")
        parser.add_argument("-p", "--page", dest='page', action='store_true', help="content pages website")
        parser.add_argument("-b", "--blog", dest="blog", action='store_true', help="blog part of website")
        parser.add_argument("-d", "--days", dest="days", help="number of days to check", type=int)
        parser.add_argument("-u","--url", dest="url", help="base url of site")
        parser.set_defaults(page=False,full=True, blog=False, days=30, url="http://dev.lco.global")

    def handle(self, **options):
        full = options.get("full")
        blog = options.get("blog")
        page = options.get("page")
        self.url = options.get("url")

        monthago = datetime.now() - timedelta(days=options.get("days"))

        if full or blog:
            logger.info('Starting Blog search')
            blogs = BlogPost.objects.filter(updated__gt=monthago)
            self.changes(blogs)
        if full or page:
            logger.info('Starting Page search')
            pages = Page.objects.filter(updated__gt=monthago)
            self.changes(pages)

    def changes(self,pages):
        for page in pages:
            if page.__class__ == BlogPost:
                url = "{}/blog/{}".format(self.url, page.slug)
            else:
                url = "{}/{}".format(self.url, page.slug)
            logger.info("{} changed {}".format(url, page.updated.isoformat()))
        return
