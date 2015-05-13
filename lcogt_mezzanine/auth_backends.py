from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.contrib.auth.models import User, check_password
from django.contrib.auth.backends import ModelBackend
import MySQLdb
import hashlib
from django.conf import settings
from lcogt.models import Profile
from django.contrib.auth.models import Group
import logging

logger = logging.getLogger(__name__)

        
def matchRBauthPass(email,password):
    # Retreive the database user information from the settings
    try:
        logger.debug(settings.DATABASES)
        rbauth = settings.DATABASES['rbauth']
        logger.debug(rbauth)
        db = MySQLdb.connect(user=rbauth['USER'], passwd=rbauth['PASSWORD'], db=rbauth['NAME'], host=rbauth['HOST'])
    except Exception as e:
        logger.debug("DB01SBA not available: %s" % e)
        return False

    # Match supplied user name to one in Drupal database
    sql_users = "SELECT username, password, first_name, last_name FROM auth_user WHERE email = '%s'" % email
    rbauth = db.cursor()
    rbauth.execute(sql_users)
    user = rbauth.fetchone()
    rbauth.close()
    db.close()
    if user:
        if check_password(password,user[1]):
            ###### If the user does not have an email address return false
            return user[0], user[1], user[2], user[3]
        else:
            logger.debug("password failed for %s" % email)
            return False
    else:
        logger.debug("User %s not found" % email)
        return False
        
def checkUserObject(email,username,password,first_name,last_name):
    try:
        user = User.objects.get(username=username)
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
        name_count = User.objects.filter(username__startswith = username).count()
        if name_count:
            username = '%s%s' % (username, name_count + 1)
        user = User.objects.create_user(username,email=email)
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.save()
#### Check there is a profile for this user
    if email.find('@lcogt') != -1:
        user.is_staff = True
        user.save()
        o,created = Profile.objects.get_or_create(user=user)
        if created:
            o.save()
        g = Group.objects.get(name='Editor') 
        g.user_set.add(user)
    return user   
         
class LCOAuthBackend(ModelBackend):         
    def authenticate(self, username=None, password=None):
        response =  matchRBauthPass(username, password)
        logger.debug(response)
        if (response):
            return checkUserObject(username,response[0],password,response[2],response[3])
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None  

            
