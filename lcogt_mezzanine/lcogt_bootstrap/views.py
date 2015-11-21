from datetime import datetime
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.forms import ModelForm
from django.views.generic import UpdateView
from django.core.urlresolvers import reverse
from django.db.models import Q
from lcogt.models import *
import logging

logger = logging.getLogger(__name__)

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
    return render(request, 'pages/userprofile.html', {'profile': profile})

def seminar_home(request):
    seminars = Seminar.objects.filter(seminardate__gt=datetime.now()).order_by('-seminardate')
    if seminars:
        nearest_seminar = seminars.order_by('seminardate')[0]
    else:
        nearest_seminar = Seminar.objects.latest('seminardate')
    return render(request,'pages/seminar_home.html',{'seminars':seminars,'nearest_seminar': nearest_seminar})

def seminar_list(request):
    seminar_list = Seminar.objects.all().order_by('-seminardate')
    paginator = Paginator(seminar_list, 25) # Show 25 seminars per page

    page = request.GET.get('page')
    try:
        seminars = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        seminars = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        seminars = paginator.page(paginator.num_pages)

    return render(request,'pages/seminar_list.html', {"seminars": seminars})

def activity_list(request):
    # Only show published i.e. status = 0 activities
    activity_list = Activity.objects.filter(status=2).order_by('title')
    paginator = Paginator(activity_list, 25) # Show 25 activities per page

    page = request.GET.get('page')
    try:
        activities = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        activities = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        activitys = paginator.page(paginator.num_pages)

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

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('userprofile',kwargs={'username':self.request.user.username})
