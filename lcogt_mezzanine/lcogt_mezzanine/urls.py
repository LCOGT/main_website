from __future__ import unicode_literals

from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView
from django.contrib import admin

from mezzanine.core.views import direct_to_template
from mezzanine.pages.views import page
from lcogt.views import UpdateProfile, SpecialPage, activity_list, people, \
    science_people, user_profile, seminar_list, seminar_home, activity_list
import biblio.views as bv


admin.autodiscover()

urlpatterns = [
    # url("^$", "mezzanine.pages.views.page", {"slug": "/"}, name="home"),
    url("^$", TemplateView.as_view(template_name='pages/index.html'), name="home"),
    url(r'^about/$', SpecialPage.as_view(), {"slug": "/about/"}, name="about"),
    url(r'^public/$', SpecialPage.as_view(template_name='public.html'), {"slug": "/public/"}, name="public"),
    url(r'^astronomers/$', SpecialPage.as_view(template_name='astronomers.html'), {"slug": "/astronomers/"}, name="astronomers"),
    url("^science/$", page, {"slug": "/science/"}, name="science"),
    url("^education/$", page, {"slug": "/education/"}, name="education"),
    url("^search/$", page, {"slug": "/search/"}, name="search"),
    url("^editprofile/$",UpdateProfile.as_view(),name="profileupdate"),
    url("^people/alumni/$", people, {'current':False}, name="oldpeople"),
    url("^people/science/$", science_people, name="scientists"),
    url("^people/$", people, {'current':True}, name="people"),
    url(r'^user/(?P<username>\w+)/$',user_profile, name="userprofile"),
    url(r'^seminar/$',seminar_home,name='seminar_home'),
    url(r'^seminar/archive/$',seminar_list,name='seminars'),
    url(r'^education/activity/$',activity_list,name='activities'),
    url(r'^observatory/visibility/$',SpecialPage.as_view(template_name='pages/visibility.html'), {"slug": "observatory/visibility"}, name="visibility"),
    url(r'^publications/$', bv.home, name='bibliohome'),
    url(r'^publications/stats/(?P<year>\d{4})/$',bv.summary,name='bibliostats_year'),
    url(r'^publications/stats/$',bv.summary,name='bibliostats'),

    # MEZZANINE'S URLS
    # ----------------
    url("^blog/", include("mezzanine.blog.urls")),
    url("^admin/", include(admin.site.urls)),
    url("^", include("mezzanine.urls")),


]

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
