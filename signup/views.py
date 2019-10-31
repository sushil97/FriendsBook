from django.shortcuts import render
from signup.forms import UserForm, UserProfileInfoForm
from signup.models import UserProfileInfo,User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/timeline/')
    else:
        return render(request, 'signup/index.html')

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'signup/registration.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})



def validate_username(request):
    username = request.GET.get('username', None)
    if User.objects.filter(username__iexact=username).exists():
        print("Username NOT available")
        return HttpResponse(True)
    else:
        print("Username Available")
        return HttpResponse(False)

def validate_email(request):
    email = request.GET.get('email', None)
    if User.objects.filter(email__iexact=email).exists():
        return HttpResponse(True)
    else:
        return HttpResponse(False)


