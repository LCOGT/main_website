from __future__ import unicode_literals
from future.builtins import int

from collections import defaultdict
from datetime import datetime, timedelta
from optparse import make_option
import re
from time import mktime, timezone
import json, pytz

from django.utils.html import linebreaks
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError
from django.utils.encoding import force_text
from django.utils.html import strip_tags

from mezzanine.blog.models import BlogPost, BlogCategory
from mezzanine.blog.management.base import BaseImporterCommand
from lcogt.utils import *

class Command(BaseImporterCommand):
    """
    Implements a Drupal importer. Takes a file path or a URL for a JSON file
    from Drupal's Node Export.
    """

    option_list = BaseImporterCommand.option_list + (
        make_option("-u", "--url", dest="url", help="URL to import file"),
        make_option("-d", "--dbname", dest="dbname", help="Name of the Drupal DB name"),
        make_option("-i", "--user", dest="user", help="Username for the Drupal DB"),
        make_option("-p", "--password", dest="password", help="Password for the Drupal DB"),
        make_option("-t", "--host", dest="host", help="Host for the Drupal DB"),
    )

    help = 'Import JSON file containing blog content'

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

        # Translate Drupal field_discipline to keywords
        categories = {'6':'education','8':'science','5143':'observatory','9':'observatory','7':'observatory'}


        #find media files from Drupal DB
        media = get_media(dbname,user,password,host)
        prompt = False
        verbosity = 2
        site = Site.objects.get_current()

        posts = []
        url = options.get("url")
        if url is None:
            raise CommandError("Usage is import_drupal_blog %s" % self.args)

        # Read the JSON in from file
        jd = open(url)
        entries = json.load(jd)

        # Convert Drupal status to Mezzanine status
        status = {'0':1,'1':2}

        for (i, entry) in enumerate(entries):
            # Get the time struct of the published date if possible and
            # the updated date if we can't.
            pub_date = datetime.fromtimestamp(int(entry['created']))

            # Tags and categories are all under "tags" marked with a scheme.
            terms = defaultdict(set)

            if entry['type'] == "blog":
                if entry['path']:
                    email = "%s@lcogt.net" % entry['name']
                    matching_user = User.objects.filter(email=email)
                    if matching_user.count() > 0:
                        mezzanine_user = matching_user[0]
                    else:
                        mezzanine_user = User.objects.get(pk=1)
                    content = replace_media_tag(entry['body']['und'][0]['value'],media)
                    blog_post = {
                        "title": force_text(entry['title'],strings_only=True),
                        "publish_date": pub_date,
                        "content": force_text(content,strings_only=True),
                        "categories": [],
                        "tags": terms["tag"],
                        "comments": [],
                        "old_url": entry['path']['alias'],
                        "user" : mezzanine_user,
                        "status" : status[entry['status']]
                    }
                    posts.append(blog_post)
        print "Found %s blog posts" % len(posts)
        for post_data in posts:
            categories = post_data.pop("categories")
            tags = post_data.pop("tags")
            comments = post_data.pop("comments")
            old_url = post_data.pop("old_url")
            post_data = self.trunc(BlogPost, prompt, **post_data)
            initial = {
                "title": "%s" % post_data.pop("title"),
                "user": post_data.pop('user'),
            }
            try:
                post, created = BlogPost.objects.get_or_create(**initial)
                if entry.get('field_discipline',None):
                    set_keywords(post, entry['field_discipline']['und'])
                for k, v in post_data.items():
                    setattr(post, k, v)
                post.allow_comments = False
                post.save()
                if created and verbosity >= 1:
                    print("Imported post: %s" % post)
                self.add_meta(post, tags, prompt, verbosity, old_url)
            except Exception, e:
                print initial['title'], e
