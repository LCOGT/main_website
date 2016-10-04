from __future__ import unicode_literals
from collections import defaultdict
from datetime import datetime, timedelta
from future.builtins import int
from mezzanine.pages.models import Page, RichTextPage
from lcogt.models import Profile
from optparse import make_option
from time import mktime, timezone
from phpserialize import loads, phpobject

from django.core.management.base import CommandError, BaseCommand
from django.utils.html import linebreaks
from django.contrib.auth.models import User, Group

from mezzanine.blog.management.base import BaseImporterCommand



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
        active = {'0':True,'1':False}
        mugshots = []
        url = options.get("url")
        if url is None:
            raise CommandError("Usage is import_drupal_spacebook %s" % self.args)

        try:
            group,created = Group.objects.get_or_create(name='Editor')
        except:
            raise CommandError("You must initialise a Group called 'Editor'")

        # Read the JSON in from file
        userdata = open(url)
        entries = loads(userdata.read(), object_hook=phpobject)
        staff = dict((v.name, v) for k,v in entries['users'].items() if len(v.roles)>1)

        for username, entry in staff.items():
            if username not in ['admin','atripp','proche','sroberts','hgomez','edward','rpiller','cwarren','ogomez','jhughes']:
                email = entry.init
                if not email or email.find('@lcogt.net') == -1:
                    email = "%s@lcogt.net" % username
                user = User.objects.create_user(username=username,email=email)
                user.set_password('darkskies0')
                if entry.field_firstname:
                    user.first_name = entry.field_firstname['und'][0]['value']
                if entry.field_lastname:
                    user.last_name = entry.field_lastname['und'][0]['value']
                user.save()
                profile,created = Profile.objects.get_or_create(user=user)
                if created:
                    text = "with "
                    if entry.field_job_title:
                        profile.job_title = entry.field_job_title['und'][0]['value']
                        text += "a job title"
                    if entry.field_about_me:
                        profile.bio = entry.field_about_me['und'][0]['value']
                        text += " and BIO"
                    if entry.picture:
                        profile.mugshot = entry.picture.filename
                        mugshots.append(entry.picture.filename)
                    if entry.field_alumnus:
                        profile.active = active[entry.field_alumnus['und'][0]['value']]
                    else:
                        profile.active = False

                    profile.save()
                    if profile.active:
                        user.is_staff = True
                        user.save()
                        group.user_set.add(user)
                else:
                    text = ""
                print "Created %s %s" % (user, text)



