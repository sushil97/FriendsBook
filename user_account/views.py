import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from signup.models import UserProfileInfo


# Create your views here.
from user_account.forms import ProfilePicUpdateForm, ProfileUpdateForm


def my_account(request):
    if request.user.is_authenticated:
        print("Request USER ID ", request.user.id)
        user = User.objects.get(id=request.user.id)
        print("Request USER ID ",user)
        user_profile = UserProfileInfo.objects.get(user_id=user.id)

        context = {
            'user': user,
            'user_profile': user_profile,
        }
        return render_to_response('profile/profile.html', context)
    else:
        return HttpResponseRedirect('/login/')


def my_timeline(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        user_profile = UserProfileInfo.objects.get(user_id=user.id)
        context ={
            'user': user,
            'user_profile': user_profile
        }
        return render_to_response('profile/timeline.html',context)
    else:
        return HttpResponseRedirect('/login/')

@csrf_exempt
def update_profile_pic(request):
    user = request.user
    if request.user.is_authenticated:
        image_form = ProfilePicUpdateForm(request.POST, request.FILES)
        if request.method == 'POST' and image_form.is_valid():
            profile = UserProfileInfo.objects.get(user_id=user.id)
            profile.profile_pic.delete(False)
            profile.profile_pic = image_form.cleaned_data['profile_pic']
            profile.save()
        return HttpResponseRedirect('/profile/')
    return HttpResponseRedirect('/login/')

@csrf_exempt
def update_bio(request):
    user = request.user
    obj = get_object_or_404(UserProfileInfo,user_id=user.id)
    if request.user.is_authenticated:
        bio_form = ProfileUpdateForm(request.POST, instance=obj)
        context={
            'bio_form': bio_form
        }
        if request.method == 'POST' and bio_form.is_valid():
            # profile = UserProfileInfo.objects.get(user_id=user.id)
            obj=bio_form.save(commit=False)
            obj.save()
            # delattr(profile, 'biography')
            # setattr(profile,'biography',bio_form)
            # profile.save()
        return HttpResponseRedirect('/profile/')
    return HttpResponseRedirect('/login/')
