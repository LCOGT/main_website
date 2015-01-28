from __future__ import unicode_literals
from future.builtins import int

from collections import defaultdict
from datetime import datetime, timedelta
from optparse import make_option
import re
from time import mktime, timezone
import json

from django.utils.html import linebreaks
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError
from django.utils.encoding import force_text
from django.utils.html import strip_tags

from mezzanine.blog.models import BlogPost, BlogCategory

from mezzanine.blog.management.base import BaseImporterCommand


class Command(BaseCommand):
    """
    Implements a Drupal importer. Takes a file path or a URL for a JSON file
    from Drupal's Node Export.
    """

    option_list = BaseImporterCommand.option_list + (
        make_option("-u", "--url", dest="url", help="URL to import file"),
    )

    categories = {'6':'education','8':'science','5143':'observatory','9':'observatory','7':'observatory'}

    def handle(self, *args, **options):
        """
        Processes the converted data into the Mezzanine database correctly.

        Attributes:
            mezzanine_user: the user to put this data in against
            date_format: the format the dates are in for posts and comments
        """
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
                    try:
                        email = "%s@lcogt.net" % entry['name']
                        mezzanine_user = User.objects.get(email=email)
                    except User.DoesNotExist:
                        mezzanine_user = User.objects.get(pk=1)
                    blog_post = {
                        "title": force_text(entry['title']),
                        "publish_date": pub_date,
                        "content": force_text(entry['body']['und'][0]['value']),
                        "categories": cat_list,
                        "tags": terms["tag"],
                        "comments": [],
                        "old_url": entry['path']['alias'],
                        "user" : mezzanine_user,
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
                "title": post_data.pop("title"),
                "user": post_data.pop('user'),
            }
            post, created = BlogPost.objects.get_or_create(**initial)
            if entry.get('field_discipline',None):
                set_keywords(entry['field_discipline']['und'])
            for k, v in post_data.items():
                setattr(post, k, v)
            post.allow_comments = False
            post.save()
            if created and verbosity >= 1:
                print("Imported post: %s" % post)
            self.add_meta(post, tags, prompt, verbosity, old_url)

def set_keywords(page, disciplines):
    for disc in disciplines:
        try:
            kw = categories[disc['nid']]
            keyword_id = Keyword.objects.get_or_create(title=kw)[0].id
            page.keywords.add(AssignedKeyword(keyword_id=keyword_id))
        except:
            pass
    return True