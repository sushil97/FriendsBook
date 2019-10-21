from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from friendship.models import Friend, FriendshipRequest
# Create your views here.
from django.urls import reverse
from signup.models import UserProfileInfo
from user_account.models import Post


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

@csrf_exempt
def show_profile(request, username=None):
    if request.user.is_authenticated and request.user.is_staff:
        auth.logout(request)
        return HttpResponseRedirect('/login/')

    elif request.user.is_authenticated and request.user.username==username:
        user = User.objects.get(id=request.user.id)
        profile = UserProfileInfo.objects.get(user_id=user.id)
        friend_requests = Friend.objects.unread_requests(user=request.user)
        posts_list = Post.objects.filter(receiver_id=user.id).order_by('-created_date')
        context = {
            'user': user,
            'friend_requests':friend_requests,
            'user_profile': profile,
            'post_lists': posts_list
        }
        return render_to_response('profile/profile.html',context)

    elif request.user.is_authenticated and request.user.username != username:
        if User.objects.filter(username=username).exists():
            this_user = User.objects.get(username=username)
            profile = UserProfileInfo.objects.get(user_id=this_user.id)
            posts_list = Post.objects.filter(receiver_id=this_user.id).order_by('-created_date')

            friends=False
            request_status=False
            friendship_id=-1
            if Friend.objects.are_friends(request.user, this_user) == True:
                friends = True
            if FriendshipRequest.objects.filter(to_user=this_user,from_user=request.user).exists():
                friendship_request = FriendshipRequest.objects.filter(to_user=this_user,from_user=request.user)
                request_status = friendship_request[0].created
                friendship_id = friendship_request[0].id
                print(request_status)
            context = {
                'user': this_user,
                'friends': friends,
                'user_profile': profile,
                'post_lists': posts_list,
                'request_status':request_status,
                'friendship_id': friendship_id
            }
            return render_to_response('profile/random_profile.html', context)
        else:
            return HttpResponseRedirect('/profile/')
    else:
        return HttpResponseRedirect('/login')
