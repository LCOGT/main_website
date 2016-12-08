from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.conf import settings
from lcogt.models import Profile
from django.contrib.auth.models import Group
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session
import json
import logging

logger = logging.getLogger(__name__)


def rbauth_login(email, password, request=None):
    client = LegacyApplicationClient(client_id=settings.CLIENT_ID)
    oauth = OAuth2Session(client=client)
    try:
        token = oauth.fetch_token(token_url=settings.RBAUTH_TOKEN_URL,
                            username=email,
                            password=password,
                            client_id=settings.CLIENT_ID,
                            client_secret=settings.CLIENT_SECRET)
        profile = oauth.get(settings.RBAUTH_PROFILE_API)
        profile = json.loads(profile.content)
    except Exception, e:
        logger.error("It broke %s" % e)
        return None

    return profile


def checkUserObject(profile, password):
    # Logging in can only be done using email address if using RBauth
    try:
        user = User.objects.get(email=profile['email'])
        user.set_password(password)
        if user.first_name != profile['first_name']:
            user.first_name == profile['first_name']
        if user.last_name != profile['last_name']:
            user.last_name == profile['last_name']
        if user.email != profile['email']:
            user.email == profile['email']
        user.save()
    except User.DoesNotExist:
        logger.error('Locating user {}'.format(profile['email']))
        # Only create a user if their email address contains "@lcogt"
        if profile['email'].find('@lco.global') != -1:
            name_count = User.objects.filter(username__startswith = profile['username']).count()
            if name_count:
                username = '%s%s' % (profile['username'], name_count + 1)
            user = User.objects.create_user(username,email=profile['email'])
            user.first_name = profile['first_name']
            user.last_name = profile['last_name']
            user.set_password(password)
            user.save()
        else:
            logger.error('User {} does not exist'.format(profile['email']))
            return None
#### Check there is a profile for this user
        user.is_staff = True
        user.save()
        o,created = Profile.objects.get_or_create(user=user)
        if created:
            o.save()
        g = Group.objects.get(name='Editor')
        g.user_set.add(user)

    return user

class LCOAuthBackend(ModelBackend):
    def authenticate(self, username=None, password=None, request=None):
        # This is only to authenticate with RBauth
        # If user cannot log in this way, the normal Django Auth is used
        response = rbauth_login(username, password)
        if (response):
            return checkUserObject(response, password)

        return None

    def get_user(self, user_id):
        try:

            return User.objects.get(pk=user_id)
        except User.DoesNotExist:

            return None
