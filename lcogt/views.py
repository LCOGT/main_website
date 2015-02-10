from django.shortcuts import render
from lcogt.models import *
from django.http import Http404
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def people(request,active=True):
    people = Profile.objects.filter(active=active).order_by('user__last_name')
    return render(request,'pages/people_list.html',{'people':people,'active':active})

def user_profile(request,username):
    try:
        profile = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        raise Http404("This user does not exist")
    return render(request, 'pages/userprofile.html', {'profile': profile})

def seminar_home(request):
    seminars = Seminar.objects.filter(seminardate__gt=datetime.now()).order_by('-seminardate')
    return render(request,'pages/seminar_home.html',{'seminars':seminars,'nearest_seminar':list(seminars)[-1]})

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

