from datetime import datetime, timedelta
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.forms import ModelForm
from django.views.generic import UpdateView, View, DetailView
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.template.response import TemplateResponse

from mezzanine.conf import settings
from mezzanine.blog.models import BlogPost, BlogCategory
from mezzanine.utils.views import paginate

from lcogt.models import *
from biblio.models import Article, Author
import logging

logger = logging.getLogger(__name__)

class SpecialPage(DetailView):
    model = LCOPage
    template = 'pages/public.html'


def people(request, current=True, scientist=False, postdoc=False):
    template = 'pages/people_list.html'
    past = None
    print(postdoc,scientist)
    if scientist or postdoc:
        people = Profile.objects.filter(scientist=scientist, post_doc=postdoc).order_by('user__last_name')
        staff = people.filter(current=True)
        past = people.filter(current=False)
    else:
        staff = Profile.objects.filter(~Q(user__username='admin'),current=current).order_by('user__last_name')
    if not current:
        template = 'pages/people_alumni.html'
    return render(request, template, {
        'people'    : staff,
        'past'      : past,
        'current'   : current,
        'scientist' : scientist,
        'postdoc'   : postdoc
        })

def user_profile(request,username):
    try:
        profile = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        raise Http404("This user does not exist")
    try:
        author = Author.objects.get(username=username)
        papers = Article.objects.filter(lcogt_authors=author)
    except:
        papers = None
    return render(request, 'pages/userprofile.html', {'profile': profile,'papers':papers})

def seminar_home(request):
    starttime = datetime.utcnow() - timedelta(minutes=360)
    seminars = Seminar.objects.filter(seminardate__gt=starttime).order_by('seminardate')
    if seminars:
        nearest_seminar = seminars.order_by('seminardate')[0]
    else:
        nearest_seminar = Seminar.objects.latest('seminardate')
    return render(request,'pages/seminar_home.html',{'seminars':seminars,'nearest_seminar': nearest_seminar})


class SeminarList(View):

    def get(self, request, *args, **kwargs):
        seminar_list = Seminar.objects.all().order_by('-seminardate')
        years = range(2016, datetime.now().year+1)

        page = request.GET.get('page')
        year = kwargs.get('year','')
        if year:
            seminar_list = seminar_list.filter(seminardate__year=year)
        paginator = Paginator(seminar_list, 25) # Show 25 seminars per page
        try:
            seminars = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            seminars = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            seminars = paginator.page(paginator.num_pages)

        return render(request,'pages/seminar_list.html', {"seminars": seminars,"years":years})

class ActivityList(View):

    def get(self, request, *args, **kwargs):
        # Only show published i.e. status = 2 activities
        activities = Activity.objects.filter(status=2).order_by('title')
        age = request.GET.get('age','all')
        if age in ['7','11','16','all']:
            if age != 'all':
                activities = activities.filter(agerange__contains=age)

        return render(request,'pages/activity_list.html', {"activities": activities})

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields=['mugshot','job_title','bio','scientist','post_doc','research_interests']

class UpdateProfile(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'pages/profile_update.html'

    def get(self, request, **kwargs):
        self.object = Profile.objects.get(user=self.request.user)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)

        return self.render_to_response(context)

    def post(self, request, **kwargs):
        profile = Profile.objects.filter(user=self.get_object())
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile.update(**form.cleaned_data)
        else:
            messages.error(request, 'The Form has errors')

        return HttpResponseRedirect(self.get_success_url())

    def get_object(self, queryset=None):

        return self.request.user

    def get_success_url(self):

        return reverse('userprofile',kwargs={'username':self.request.user.username})

class SpaceBook(View):
    template_name = 'pages/spacebook.html'

    def get(self, request, *args, **kwargs):
        chapters = SpacePage.objects.filter(parent_id=821)
        return render(request, self.template_name, {"chapters": chapters})


class PartnersView(View):
    template_name = 'pages/partners.html'

    def get(self, request, *args, **kwargs):
        active = kwargs.get('active',True)
        partners = PartnerPage.objects.filter(active=active)
        print("here")
        return render(request, self.template_name, {"partners": partners, "active":active})


def lco_blog_post_list(request, tag=None, year=None, month=None, username=None,
                   category=None, template="blog/blog_post_list.html",
                   extra_context=None):
    """
    Display a list of blog posts that are filtered by tag, year, month,
    author or category.
    """
    templates = []
    blog_posts = BlogPost.objects.published(for_user=request.user)

    if category is not None:
        category = get_object_or_404(BlogCategory, slug=category)
        blog_posts = blog_posts.filter(categories=category)
        templates.append(u"blog/blog_post_list_%s.html" %
                          str(category.slug))
    if category == None:
        blog_posts = blog_posts.filter(categories=None)
    author = None
    if username is not None:
        author = get_object_or_404(User, username=username)
        blog_posts = blog_posts.filter(user=author)
        templates.append(u"blog/blog_post_list_%s.html" % username)

    prefetch = ("categories", "keywords__keyword")
    blog_posts = blog_posts.select_related("user").prefetch_related(*prefetch)
    blog_posts = paginate(blog_posts, request.GET.get("page", 1),
                          settings.BLOG_POST_PER_PAGE,
                          settings.MAX_PAGING_LINKS)
    context = {"blog_posts": blog_posts, "year": year, "month": month,
               "tag": tag, "category": category, "author": author}
    context.update(extra_context or {})
    templates.append(template)
    return TemplateResponse(request, templates, context)
