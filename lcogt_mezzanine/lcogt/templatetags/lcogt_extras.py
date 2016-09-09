from django import template
from mezzanine.galleries.models import GalleryImage
from random import randint
from datetime import timedelta, datetime
from mezzanine.pages.models import Page
from django.urls import reverse

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

@register.filter
def headerbar_image(keywords):
    if 'education' in keywords or 'public' in keywords or 'spacebook' in keywords:
        images = GalleryImage.objects.filter(gallery__title__icontains='astronomical')
    elif 'science' in keywords or 'scientists' in keywords or 'research' in keywords:
        images = GalleryImage.objects.filter(gallery__title__icontains='observatory')
    elif 'observatory' in keywords or 'network' in keywords or 'engineering' in keywords or 'operations' in keywords:
        images = GalleryImage.objects.filter(gallery__title__icontains='technical')
    else:
        images = GalleryImage.objects.all()
    try:
        image = images[randint(0, images.count() - 1)]
        return image.file
    except ValueError:
        return ''

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
	print(modelname, objectid)
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
