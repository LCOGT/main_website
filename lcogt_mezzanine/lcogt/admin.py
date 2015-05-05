from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from mezzanine.pages.models import RichTextPage
from mezzanine.galleries.models import Gallery
from mezzanine.forms.models import  Form
from mezzanine.blog.models import BlogPost
from .models import Activity, Seminar, Profile, LCOPage

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

import reversion

class PageReversion(PageAdmin, reversion.VersionAdmin):
    pass

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'user profiles'
    max_num = 1

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (ProfileInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Activity, PageReversion)
admin.site.register(Seminar, PageReversion)
admin.site.register(LCOPage, PageReversion)
reversion.register(BlogPost)
reversion.register(RichTextPage)
reversion.register(Form)
reversion.register(Gallery)

