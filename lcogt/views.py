from django.shortcuts import render
from lcogt.models import *
from django.http import Http404

def people(request,active=True):
	people = Profile.objects.filter(active=active).order_by('user__last_name')
	return render(request,'pages/people_list.html',{'people':people,'active':active})

def user_profile(request,username):
    try:
        profile = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        raise Http404("This user does not exist")
    return render(request, 'pages/userprofile.html', {'profile': profile})
