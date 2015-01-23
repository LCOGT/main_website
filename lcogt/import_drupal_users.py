from __future__ import unicode_literals
from collections import defaultdict
from datetime import datetime, timedelta
from future.builtins import int
from mezzanine.pages.models import Page, RichTextPage
from lcogt.models import Profile
from optparse import make_option
from time import mktime, timezone
import json
import re
import MySQLdb

from django.core.management.base import CommandError, BaseCommand
from django.utils.html import linebreaks
from django.contrib.auth.models import User
from optparse import make_option


class Command(BaseImporterCommand):
    """
    Implements a Drupal importer. Takes a file path or a URL for a JSON file
    from Drupal's Node Export i.e.
    ./drush node-export --type=book --format=json --file=book.json
    """

    option_list = BaseImporterCommand.option_list + (
        make_option("-u", "--url", dest="url", help="URL to import file"),
    )

    help = 'Import JSON files containing Drupal Users'

    def handle_import(self, options):
        url = options.get("url")
        if url is None:
            raise CommandError("Usage is import_drupal_spacebook %s" % self.args)

        # Read the JSON in from file
        js = open(url)
        users = json.load(jd)
        staff = [u for u in users if u['data'] and u['data'].find('ldap') != -1]
        profiles = {u['name'] : u['field_about_me'] for u in staff if u['type']=='user_profile'}
        jobs = {u['name'] : u['field_job_title'] for u in staff if u['type']=='staff_profile'}

        for user, bio in profiles.items():
            if user not in ['admin','atripp','proche','sroberts','hgomez','edward','rpiller']:
                email = "%s@lcogt.net" % user
                user = User.objects.create_user(username=user,email=email)
                user.set_password('password')
                user.save()
                profile,created = Profile.objects.get_or_create(user=user)
                if created:
                    text = "with "
                    job = jobs.get(user, None)
                    if job:
                        profile.job_title = job['und'][0]['value']
                        text += "a job title"
                    if bio:
                        profile.bio = bio['und'][0]['value']
                        text += " and BIO"
                    profile.save()
                else:
                    text = ""
                print "Created %s %s" % (user, text)



def update_user(entry,user):
    if user:
        rt,created = Profile.objects.get_or_create(user=user)
        if created:
            rt.bio = entry['field_about_me']['und'][0]['value']
            rt.job_title = entry['']
            rt.save()
        return True
    else:
        return None

