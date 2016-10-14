from django.core.management.base import CommandError, BaseCommand
from bs4 import BeautifulSoup
from urlparse import urljoin
from mezzanine.pages.models import Page
from mezzanine.blog.models import BlogPost
from lcogt.models import Activity, Seminar

import logging
import requests

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
        parser.add_argument("-u","--url", dest="url", help="base url of site")
        parser.add_argument("-i", "--images", dest="images", action='store_true', help="check images")
        parser.set_defaults(page=False,full=False, blog=False, images=False, url="http://lco.global")

    def handle(self, **options):
        full = options.get("full")
        blog = options.get("blog")
        page = options.get("page")
        self.url = options.get("url")
        self.images = options.get("images")

        if full or blog:
            logger.info('Starting Blog search')
            blogs = BlogPost.objects.filter(status=2)
            self.find_links(blogs)
        if full or page:
            logger.info('Starting Page search')
            pages = Page.objects.filter(status=2,id__gt=389)
            self.find_links(pages)

    def find_links(self,pages):
        for page in pages:
            if page.__class__ == BlogPost:
                content = page.content
            elif page.__dict__['content_model'] == 'activity':
                content = page.get_content_model().full_text
            elif page.__dict__['content_model'] == 'seminar':
                content = page.get_content_model().speaker_biog
            else:
                try:
                    content = page.get_content_model().content
                except AttributeError:
                    logger.error("Problem with {}".format(page.slug))
                    continue
            soup = BeautifulSoup(content, 'html.parser')
            for link in soup.find_all('a'):
                self.test_link(link.get('href'),page)
            if self.images:
                for link in soup.find_all('img'):
                    self.test_link(link.get('src'), page)
        return

    def test_link(self, path, referrer):
        if not path:
            logger.error('{} is invalid: {} {}'.format(path, referrer.id, referrer.slug))
            return
        if 'mailto' in path:
            return
        if path[0] != 'h':
            path = urljoin(self.url,path)
        try:
            req = requests.get(path, timeout=10)
        except requests.exceptions.Timeout:
            logger.error('{} timed out on {}'.format(path, referrer.slug))
            return
        except requests.exceptions.ConnectionError:
            logger.error('{} not found {}'.format(path, referrer.slug))
            return
        if req.status_code in [404, 500, 403]:
            logger.error('{}/{} gave code {} for {}'.format(self.url, referrer.slug, req.status_code, path))
            return
        return
