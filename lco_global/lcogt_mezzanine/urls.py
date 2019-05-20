from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView
from django.contrib import admin
from django.contrib.staticfiles import views
from django.conf.urls.static import static

from mezzanine.core.views import direct_to_template
from mezzanine.pages.views import page
import mezzanine.blog.views as blogv
from lcogt.views import UpdateProfile, SpecialPage, ActivityList, people, \
    user_profile, seminar_home, SeminarList, SpaceBook, lco_blog_post_list, \
    PartnersView
import biblio.urls

# Add the urlpatterns for any custom Django applications here.
# You can also change the ``home`` view to add your own functionality
# to the project's homepage.

admin.autodiscover()

urlpatterns = [
    # url("^$", "mezzanine.pages.views.page", {"slug": "/"}, name="home"),
    url(r"^$", SpecialPage.as_view(template_name='pages/index.html'), {"slug": "/"}, name="home"),
    url(r'^about/$', SpecialPage.as_view(template_name='about.html'), {"slug": "/about/"}, name="about"),
    url(r'^everyone/$', page, {"slug": "/public/"}, name="everyone"),
    url(r'^astronomers/$', page, {"slug": "/astronomers/"}, name="astronomers"),
    url(r'^science/$', page, {"slug": "/science/"}, name="science"),
    url(r'^education/$', page, {"slug": "/education/"}, name="education"),
    url(r'^search/$', page, {"slug": "/search/"}, name="search"),
    url(r'^editprofile/$',UpdateProfile.as_view(),name="profileupdate"),
    url(r'^people/alumni/$', people, {'current':False}, name="oldpeople"),
    url(r'^people/science/$', people, {'current':True, 'scientist':True}, name="scientists"),
    url(r'^people/postdocs/$', people, {'current':True, 'postdoc':True}, name="postdocs"),
    url(r'^people/$', people, {'current':True}, name="people"),
    url(r'^user/(?P<username>\w+)/$',user_profile, name="userprofile"),
    url(r'^seminar/$',seminar_home,name='seminar_home'),
    url(r'^seminar/archive/(?P<year>[0-9]+)/$',SeminarList.as_view(),name='seminars_year'),
    url(r'^seminar/archive/$',SeminarList.as_view(),name='seminars'),
    url(r'^education/activity/$',ActivityList.as_view(),name='activities'),
    url(r'^education/partners/$', PartnersView.as_view(), name="partners"),
    url(r'^observatory/visibility/$',SpecialPage.as_view(template_name='pages/visibility.html'), {"slug": "observatory/visibility"}, name="visibility"),
    url(r'^spacebook/$',SpaceBook.as_view(), name='spacebook'),
    url(r'^publications/', include(biblio.urls)),

    # Announcement URL structure in News
    # ----------------
    url(r"^", include("mezzanine.urls")),
    url("^news/category/(?P<category>.*)/$", blogv.blog_post_list, name="blog_post_list_category"),
    url("^news/(?P<slug>.*)/$", blogv.blog_post_detail, name="blog_post_detail"),
    url("^news/$", lco_blog_post_list, name="blog_post_list"),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls'))
    ]


# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"

if settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', views.serve),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
