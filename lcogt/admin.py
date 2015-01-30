from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from .models import Activity, Seminar, Profile, LCOPage

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


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

admin.site.register(Activity, PageAdmin)
admin.site.register(Seminar, PageAdmin)
admin.site.register(LCOPage, PageAdmin)

