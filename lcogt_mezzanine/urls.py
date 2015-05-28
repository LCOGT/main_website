from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

from mezzanine.core.views import direct_to_template
from lcogt.views import UpdateProfile


admin.autodiscover()

# Add the urlpatterns for any custom Django applications here.
# You can also change the ``home`` view to add your own functionality
# to the project's homepage.

urlpatterns = i18n_patterns("",
    # Change the admin prefix here to use an alternate URL for the
    # admin interface, which would be marginally more secure.
    ("^admin/", include(admin.site.urls)),
)

urlpatterns += patterns('',

    # We don't want to presume how your homepage works, so here are a
    # few patterns you can use to set it up.

    # HOMEPAGE AS AN EDITABLE PAGE IN THE PAGE TREE
    # ---------------------------------------------
    # This pattern gives us a normal ``Page`` object, so that your
    # homepage can be managed via the page tree in the admin. If you
    # use this pattern, you'll need to create a page in the page tree,
    # and specify its URL (in the Meta Data section) as "/", which
    # is the value used below in the ``{"slug": "/"}`` part.
    # Also note that the normal rule of adding a custom
    # template per page with the template name using the page's slug
    # doesn't apply here, since we can't have a template called
    # "/.html" - so for this case, the template "pages/index.html"
    # should be used if you want to customize the homepage's template.

    url("^$", "mezzanine.pages.views.page", {"slug": "/"}, name="home"),
    url("^public$", "mezzanine.pages.views.page", {"slug": "/public/"}, name="public"),
    url("^astronomers$", "mezzanine.pages.views.page", {"slug": "/astronomers/"}, name="astronomers"),
    url("^science$", "mezzanine.pages.views.page", {"slug": "/science/"}, name="science"),
    url("^search/$", "mezzanine.pages.views.page", {"slug": "/search/"}, name="search"),
    url("^editprofile/$",UpdateProfile.as_view(),name="profileupdate"),
    url("^people/alumni/$", "lcogt.views.people", {'current':False}, name="oldpeople"),
    url("^people/science/$", "lcogt.views.science_people", name="scientists"),
    url("^people/$", "lcogt.views.people", {'current':True}, name="people"),
    url(r'^user/(?P<username>\w+)/$',"lcogt.views.user_profile", name="userprofile"),
    url(r'^seminar/$','lcogt.views.seminar_home',name='seminar_home'),
    url(r'^seminar/archive/$','lcogt.views.seminar_list',name='seminars'),
    url(r'^education/activity/$','lcogt.views.activity_list',name='activities'),
    url(r'^publications/$', 'biblio.views.home', name='bibliohome'),
    url(r'publications/stats/(?P<year>\d{4})/$','biblio.views.summary',name='bibliostats_year'),
    url(r'publications/stats/$','biblio.views.summary',name='bibliostats'),

    # MEZZANINE'S URLS
    # ----------------
    # ADD YOUR OWN URLPATTERNS *ABOVE* THE LINE BELOW.
    # ``mezzanine.urls`` INCLUDES A *CATCH ALL* PATTERN
    # FOR PAGES, SO URLPATTERNS ADDED BELOW ``mezzanine.urls``
    # WILL NEVER BE MATCHED!

    # If you'd like more granular control over the patterns in
    # ``mezzanine.urls``, go right ahead and take the parts you want
    # from it, and use them directly below instead of using
    # ``mezzanine.urls``.
    ("^", include("mezzanine.urls")),


)

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
