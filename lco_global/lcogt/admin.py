from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from mezzanine.pages.admin import PageAdmin
from mezzanine.pages.models import RichTextPage, Page
from mezzanine.galleries.models import Gallery
from mezzanine.forms.models import  Form
from mezzanine.blog.models import BlogPost
from mezzanine.blog.admin import BlogPostAdmin

from lcogt.models import Activity, Seminar, Profile, LCOPage, SpacePage, PartnerPage

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.forms import CheckboxSelectMultiple

from reversion.admin import VersionAdmin

class PageReversion(PageAdmin, VersionAdmin):
    pass


class LCOBlogAdmin(BlogPostAdmin):
    fieldsets =  (
        (None, {
            "fields": ["title", "status", "publish_date", "categories", "slug", ("description", "gen_description"), "featured_image", "content"],
        }),
        (_("Meta data"), {
            "fields": ["_meta_title",
                        "keywords"],
            "classes": ("collapse-closed",)
        }),
    )
    filter_horizontal = () # Overrides the default

class PartnerAdmin(PageAdmin):
    fieldsets =  (
        (None, {
            "fields": ["title", "status", "start", "end", "active", "content", "outputs",
                        "organizers", "organization", "partner_logo", "partner_site", "contact",
                        "audience_type","region"],
        }),
        (_("Meta data"), {
            "fields": ["_meta_title",
                        "keywords", "publish_date", "slug"],
            "classes": ("collapse-closed",)
        }),
    )

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'user profiles'
    max_num = 1

def make_postdoc(self,request,queryset):
	for item in queryset:
		item.profile.post_doc = True
		item.profile.save()
	self.message_user(request,"Added %s people as postdocs" % queryset.count())
make_postdoc.short_description = "Change to PostDoc"

def make_staff_scientist(self,request,queryset):
	for item in queryset:
		item.profile.scientist = True
		item.profile.save()
	self.message_user(request,"Added %s people as staff scientists" % queryset.count())
make_staff_scientist.short_description = "Change to Staff Scientist"

def not_current_staff(self,request,queryset):
    for item in queryset:
        item.profile.current = False
        item.profile.save()
    self.message_user(request,"Changed %s people to not current staff" % queryset.count())
not_current_staff.short_description = "Change to not current staff"

# Define a new User admin
class UserAdmin(UserAdmin):
    list_display = ['last_name','first_name','_scientist','_post_doc','_current_staff']
    inlines = (ProfileInline, )
    actions = [make_staff_scientist, make_postdoc, not_current_staff]
    ordering = ['last_name']

    def _scientist(self,obj):
        if Profile.objects.get(user=obj).scientist:
            return True
        else:
            return False
    _scientist.boolean = True
    _scientist.short_description = 'Staff Scientist'

    def _post_doc(self,obj):
        if Profile.objects.get(user=obj).post_doc:
            return True
        else:
            return False
    _post_doc.boolean = True
    _post_doc.short_description = 'Post Doc'

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

admin.site.unregister(BlogPost)
admin.site.register(BlogPost, LCOBlogAdmin)

admin.site.register(Seminar, PageReversion)
admin.site.register(LCOPage, PageReversion)
admin.site.register(Activity)#, PageReversion)
admin.site.register(SpacePage)#, PageReversion)
admin.site.register(PartnerPage, PartnerAdmin)
