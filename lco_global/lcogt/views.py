from datetime import datetime, timedelta
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.forms import ModelForm
from django.views.generic import UpdateView, View, DetailView
from django.core.urlresolvers import reverse
from django.db.models import Q
from lcogt.models import *
from biblio.models import Article, Author
import logging

logger = logging.getLogger(__name__)

class SpecialPage(DetailView):
    model = LCOPage
    template = 'pages/public.html'


def science_people(request):
    people = Profile.objects.filter(science_team=True,current=True).order_by('user__last_name')
    return render(request,'pages/people_list.html',{'people':people,'science':True,'current': True})

def people(request,current=True):
    people = Profile.objects.filter(~Q(user__username='admin'),current=current).order_by('user__last_name')
    return render(request,'pages/people_list.html',{'people':people,'current':current})

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
        if age in ['6','11','16','all']:
            if age != 'all':
                activities = activities.filter(agerange__contains=age)
        return render(request,'pages/activity_list.html', {"activities": activities})

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields=['mugshot','job_title','bio','science_team','research_interests']

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
