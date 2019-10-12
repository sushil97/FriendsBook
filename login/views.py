from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response

# Create your views here.
from django.urls import reverse
from signup.models import UserProfileInfo


@login_required
def special(request):
    return HttpResponse("You are logged in !")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        #identity = User.objects.only('id').get(username=username).id
        #print(identity)
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                # user_profile = UserProfileInfo.objects.get(id=user.id)
                context = {
                    'user': user,
                    # 'user_profile': user_profile
                }
                #userprofileinfo = UserProfileInfo.objects.filter(user_id=identity)
                # return HttpResponseRedirect(reverse('index'), context)
                return HttpResponseRedirect('/profile/')
                #return render_to_response('profile/timeline.html', context)
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'signup/login.html', {})