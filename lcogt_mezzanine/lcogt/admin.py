from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from mezzanine.pages.models import RichTextPage
from mezzanine.galleries.models import Gallery
from mezzanine.forms.models import  Form
from mezzanine.blog.models import BlogPost
from lcogt.models import Activity, Seminar, Profile, LCOPage

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from reversion.admin import VersionAdmin

class PageReversion(PageAdmin, VersionAdmin):
    pass

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'user profiles'
    max_num = 1

def make_science_staff(self,request,queryset):
	for item in queryset:
		item.profile.science_team = True
		item.profile.save()
	self.message_user(request,"Added %s people to science team" % queryset.count())
make_science_staff.short_description = "Add to science team"

def not_current_staff(self,request,queryset):
    for item in queryset:
        item.profile.current = False
        item.profile.save()
    self.message_user(request,"Changes %s people to not current staff" % queryset.count())
not_current_staff.short_description = "Change to not current staff"

# Define a new User admin
class UserAdmin(UserAdmin):
    list_display = ['last_name','first_name','_science_team','_current_staff']
    inlines = (ProfileInline, )
    actions = [make_science_staff,not_current_staff]

    def _science_team(self,obj):
        if Profile.objects.get(user=obj).science_team:
            return True
        else:
            return False
    _science_team.boolean = True
    _science_team.short_description = 'Science Staff?'

    def _current_staff(self,obj):
        if Profile.objects.get(user=obj).current:
            return True
        else:
            return False
    _current_staff.boolean = True
    _current_staff.short_description = 'Current Staff?'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Activity, PageReversion)
admin.site.register(Seminar, PageReversion)
admin.site.register(LCOPage, PageReversion)
