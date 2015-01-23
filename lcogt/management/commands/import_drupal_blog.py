from __future__ import unicode_literals
from future.builtins import int

from collections import defaultdict
from datetime import datetime, timedelta
from optparse import make_option
import re
from time import mktime, timezone
import json

from django.core.management.base import CommandError
from django.utils.html import linebreaks
from django.contrib.auth.models import User

from mezzanine.blog.management.base import BaseImporterCommand


class Command(BaseImporterCommand):
    """
    Implements a Drupal importer. Takes a file path or a URL for a JSON file
    from Drupal's Node Export.
    """

    option_list = BaseImporterCommand.option_list + (
        make_option("-u", "--url", dest="url", help="URL to import file"),
    )

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
            raise CommandError("Usage is import_drupal_blog %s" % self.args)

        # Read the JSON in from file
        jd = open(url)
        entries = json.load(jd)

        for (i, entry) in enumerate(entries):
            # Get the time struct of the published date if possible and
            # the updated date if we can't.
            pub_date = datetime.fromtimestamp(int(entry['created']))

            # Tags and categories are all under "tags" marked with a scheme.
            terms = defaultdict(set)
            cat_list = []
            for item in getattr(entry['field_discipline'], "und", []):
                cat = categories.getattr(item,None)
                if cat:
                    cat_list.append(cat)

            if entry['type'] == "blog":
                if entry['path']:
                    # print (entry['body']['und'][0]['value'])
                    # print (pub_date,terms["tag"], ",".join(cat_list),entry['path']['alias'])
                    post = self.add_post(title=entry['title'], content=entry['body']['und'][0]['value'],
                                         pub_date=pub_date, tags=terms["tag"],
                                         categories=",".join(cat_list),
                                         old_url=entry['path']['alias'])
                    # Correct author 
                    try:
                        email = "%s@lcogt.net" % entry['name']
                        mezzanine_user = User.objects.filter(username=email)
                    except User.DoesNotExist:
                        raise CommandError("Invalid Mezzanine user: %s" % email)
                else:
                    print "********* %s *********" % entry['title']




