from django import template
from mezzanine.galleries.models import GalleryImage
from random import randint
from datetime import timedelta, datetime
from mezzanine.pages.models import Page
from django.urls import reverse
from django.conf import settings
import logging
import os

logger = logging.getLogger(__name__)

register = template.Library()

@register.filter
def body_class(keywords):
    lower_keys = [x.title.lower() for x in keywords]
    if 'education' in lower_keys or 'public' in lower_keys:
        return 'education'
    elif 'science' in lower_keys or 'scientists' in lower_keys or 'research' in lower_keys:
        return 'science'
    elif 'observatory' in lower_keys or 'network' in lower_keys or 'engineering' in lower_keys or 'operations' in lower_keys:
        return 'observatory'
    else:
        return 'home'

@register.simple_tag
def headerbar_image():
    images = GalleryImage.objects.all()
    try:
        image = images[randint(0, images.count() - 1)]
        return image.file
    except ValueError:
        logger.error('Did not find GalleryImage: {}'.format(images))
        return '/files/galleries/astrophotography/m104_bfulton.jpg'

@register.filter
def is_spacebook(keywords):
    lower_keys = [x.title.lower() for x in keywords]
    if 'spacebook' in lower_keys:
        return True
    else:
        return False

@register.simple_tag
def recent_edits(days):
    dtime = timedelta(days)
    now = datetime.now()
    pages = Page.objects.filter(updated__gte= (now - dtime))
    return pages

@register.filter
def rev_admin_url(modelname, objectid):
	if modelname in ['richtextpage','page']:
		rev_text = "admin:pages_{}_change".format(modelname)
	elif modelname == 'gallery':
		rev_text = "admin:galleries_{}_change".format(modelname)
	elif modelname == 'blog':
		rev_text = "admin:blog_{}_change".format(modelname)
	else:
		rev_text = "admin:lcogt_{}_change".format(modelname)
	try:
		change_url = reverse(rev_text, args=(objectid,))
		return change_url
	except:
		return ''
