from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.contrib.auth.models import User, check_password
from django.contrib.auth.backends import ModelBackend
import MySQLdb
import hashlib
from django.conf import settings
from lcogt.models import Profile
from django.contrib.auth.models import Group
from oauthlib.oauth2 import BackendApplicationClient
from django_tools.middlewares import ThreadLocal
import logging

logger = logging.getLogger(__name__)


def rbauth_login(email, password):
    client = BackendApplicationClient(client_id=settings.CLIENT_ID)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=settings.RBAUTH_TOKEN_URL,
                            username=email,
                            password=password,
                            client_id=settings.CLIENT_ID,
                            client_secret=settings.CLIENT_SECRET)
    return token

def checkUserObject(email,username,password,first_name,last_name):
    # Logging in can only be done using email address if using RBauth
    try:
        user = User.objects.get(email=email)
        if not check_password(password,user.password):
            user.set_password(password)
        if user.first_name != first_name:
            user.first_name == first_name
        if user.last_name != last_name:
            user.last_name == last_name
        if user.email != email:
            user.email == email
        user.save()
    except User.DoesNotExist:
        # Only create a user if their email address contains "@lcogt"
        if email.find('@lcogt') != -1:
            name_count = User.objects.filter(username__startswith = username).count()
            if name_count:
                username = '%s%s' % (username, name_count + 1)
            user = User.objects.create_user(username,email=email)
            user.first_name = first_name
            user.last_name = last_name
            user.set_password(password)
            user.save()
        else:
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

def get_odin_cookie_proposals(email, password):
    '''
    Use login credentials to login to ODIN as well and add sessionid to Messier Bingo session
    while the session is open get the user's proposal list
    '''
    client = requests.session()
    url = 'https://lcogt.net/observe/auth/accounts/login/'
    r = requests.get(url)
    token = r.cookies['csrftoken']
    r = client.post(url, data={'username':email,'password':password, 'csrfmiddlewaretoken' : token}, cookies={'csrftoken':token})
    try:
        page = client.get('http://lcogt.net/observe/proposal/', timeout=20.0)
        proposals = get_epo_proposals(page)
    except requests.exceptions.ReadTimeout:
        logger.error('Could not obtain proposals. Timed out.')
    try:
        request = ThreadLocal.get_current_request()
        request.session['odin.sessionid'] = client.cookies['odin.sessionid']
        return proposals
    except Exception, e:
        logger.error(client.cookies)
        return False

class LCOAuthBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        # This is only to authenticate with RBauth
        # If user cannot log in this way, the normal Django Auth is used
        response = rbauth_login(username, password)
        if (response):
            return checkUserObject(username,response[0],password,response[2],response[3])
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
