from django import template

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
def is_spacebook(keywords):
	lower_keys = [x.title.lower() for x in keywords]
	if 'spacebook' in lower_keys:
		return True
	else:
		return False
