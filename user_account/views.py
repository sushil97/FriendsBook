from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from signup.models import UserProfileInfo


# Create your views here.
def my_account(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        user_profile = UserProfileInfo.objects.get(id=user.id)
        context = {
            'user': user,
            'user_profile': user_profile,
        }
        return render_to_response('profile/profile.html', context)
    else:
        return HttpResponseRedirect('/login/')
