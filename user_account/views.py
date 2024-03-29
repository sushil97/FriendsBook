import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from groups.models import GroupRequestInfo, GroupProfileInfo
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.utils import timezone
from pages.models import PageFollowInfo, PageProfileInfo, PagePost
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from user_account.models import Post
from user_account.forms import PostForm
from user_account.forms import PrivacyInfoForm
from friendship.exceptions import AlreadyExistsError
from django.conf import settings
from signup.models import UserProfileInfo
from friendship.models import Friend, FriendshipRequest

# Create your views here.
from user_account.forms import ProfilePicUpdateForm, ProfileUpdateForm


def my_account(request):
    if request.user.is_authenticated:
        print("Request USER ID ", request.user.id)
        user = User.objects.get(id=request.user.id)
        print("Request USER ID ", user)
        user_profile = UserProfileInfo.objects.get(user_id=user.id)
        posts_list = Post.objects.filter(receiver_id=user.id).order_by('-created_date')
        context = {
            'user': user,
            'user_profile': user_profile,
            'post_lists': posts_list
        }
        return render_to_response('profile/profile.html', context)
    else:
        return HttpResponseRedirect('/login/')


@csrf_exempt
def my_timeline(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        user_profile = UserProfileInfo.objects.get(user_id=user.id)
        friends_list = Friend.objects.friends(request.user)
        friend_users = []
        friend_users = friends_list.copy()  # copy to prevent the change of list of friends
        friend_users.insert(0, user)
        posts_list = Post.objects.all().order_by('-created_date')
        group_list = Group.objects.filter(user=request.user)
        my_pages_list = PageProfileInfo.objects.filter(admin=request.user)
        following_pages_list = PageFollowInfo.objects.filter(from_user=request.user)
        context = {
            'user': user,
            'user_profile': user_profile,
            'friends_list': friends_list,
            'post_lists': posts_list,
            'group_lists': group_list,
            'friend_users': friend_users,
            'my_pages_list': my_pages_list,
            'following_pages_list': following_pages_list
        }
        return render_to_response('profile/timeline.html', context)
    else:
        return HttpResponseRedirect('/login/')


@csrf_exempt
def update_profile_pic(request):
    user = request.user
    default = 'default_pic/default_pic.jpg'
    if request.user.is_authenticated:
        image_form = ProfilePicUpdateForm(request.POST, request.FILES)
        if request.method == 'POST' and image_form.is_valid():
            profile = UserProfileInfo.objects.get(user_id=user.id)
            if profile.profile_pic == default:
                profile.profile_pic = image_form.cleaned_data['profile_pic']
                profile.save()
            else:
                profile.profile_pic.delete(False)
                profile.profile_pic = image_form.cleaned_data['profile_pic']
                profile.save()
        return HttpResponseRedirect('/profile/')
    return HttpResponseRedirect('/login/')


@csrf_exempt
def update_bio(request):
    user = request.user
    obj = get_object_or_404(UserProfileInfo, user_id=user.id)
    if request.user.is_authenticated:
        bio_form = ProfileUpdateForm(request.POST, instance=obj)
        context = {
            'bio_form': bio_form
        }
        if request.method == 'POST' and bio_form.is_valid():
            # profile = UserProfileInfo.objects.get(user_id=user.id)
            obj = bio_form.save(commit=False)
            obj.save()
            # delattr(profile, 'biography')
            # setattr(profile,'biography',bio_form)
            # profile.save()
        return HttpResponseRedirect('/profile/')
    return HttpResponseRedirect('/login/')


@csrf_exempt
def privacy_info(request):
    user = request.user
    obj = get_object_or_404(UserProfileInfo, user_id=user.id)
    userprofile = UserProfileInfo.objects.get(user=user)
    if request.user.is_authenticated:
        privacy_form = PrivacyInfoForm(request.POST, instance=obj)
        print(privacy_form.is_valid())
        if request.method == 'POST':
            if privacy_form.is_valid():
                obj = privacy_form.save(commit=False)
                obj.save()
                return HttpResponseRedirect('/profile/')
            else:
                print(privacy_form.errors)
                return HttpResponseRedirect('/settings/privacy/')
        else:
            return render_to_response('settings/privacy.html',{'user':request.user, 'userprofile':userprofile})
    else:
        return HttpResponseRedirect('/login/')


def search(request):
    if request.user.is_authenticated and request.method == 'GET':
        user = request.user
        query = request.GET.get('search')
        users_list = User.objects.filter(
            Q(username__contains=query) | Q(email=query) | Q(first_name__contains=query) | Q(last_name__contains=query),
            is_staff=False)
        groups_list = Group.objects.filter(Q(name__contains=query))
        pages_info_list = PageProfileInfo.objects.filter(Q(page__contains=query))
        users_info_list = []
        groups_info_list = []
        users_info_list = UserProfileInfo.objects.none()
        groups_info_list = GroupProfileInfo.objects.none()
        for i in users_list:
            userid = i.id
            queryset = UserProfileInfo.objects.filter(Q(user_id=userid))
            users_info_list = users_info_list | queryset

        for i in groups_list:
            groupid = i.id
            queryset = GroupProfileInfo.objects.filter(Q(group_id=groupid))
            groups_info_list = groups_info_list | queryset
        print(users_info_list)
        print(groups_info_list)
        print(pages_info_list)
        context = {
            'user': user,
            'this_user_list': users_list,
            'this_user_profile_list': users_info_list,
            'query': query,
            'groups_info_list': groups_info_list,
            'groups_list': groups_list,
            'pages_info_list': pages_info_list
        }
        return render_to_response('profile/search.html', context)
    else:
        return HttpResponseRedirect('/login')


@csrf_exempt
def create_post(request):
    user = request.user
    if request.method == 'POST':
        post_form = PostForm(data=request.POST)
        print(post_form)
        if user.is_authenticated:
            post_form = PostForm(data=request.POST)
            print(post_form)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.author = user
                post.receiver = user
                post.save()
            else:
                print(post_form.errors)
        else:
            return HttpResponseRedirect("/login/")
    return HttpResponseRedirect("/timeline/")


@csrf_exempt
def create_profile_post(request, username=None):
    user = request.user
    print(username)
    if user.is_authenticated:
        if request.method == 'POST' and request.user.username != username and User.objects.filter(
                username=username).exists():
            this_user = User.objects.get(username=username)
            post_form = PostForm(data=request.POST)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.author = user
                post.receiver = this_user
                post.save()
            else:
                print(post_form.errors)
            return HttpResponseRedirect('/profile/' + username + '/')
        return HttpResponseRedirect('/timeline/')
    else:
        return HttpResponseRedirect("/timeline/")


def accountsettings(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            userProfile = User.objects.get(username=request.user.username)

        context = {
            'userProfile': userProfile
        }
        return render(request, 'settings/account_settings.html', context)
    else:
        return HttpResponseRedirect('/timeline/')


def account_settings(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fname = request.POST['f_name']
            lname = request.POST['l_name']
            email = request.POST['email']
            user = User.objects.get(username=request.user.username)
            user.first_name = fname
            user.last_name = lname
            user.email = email
            user.save()
            return HttpResponseRedirect('/settings/account/')
        else:
            return HttpResponseRedirect('/settings/account/')
    else:
        return HttpResponseRedirect('/login/')


def change_password(request):
    if request.user.is_authenticated:

        if request.method == "POST":
            current = request.POST['current']
            new = request.POST['new']
            new1 = request.POST['new1']
            user = User.objects.get(username=request.user.username)
            existing_pswrd = request.user.password
            print("Hi")
            if user.check_password(current):
                print("existing is rt")
                if str(new) == str(new1):
                    user.set_password(new)
                    user.save()
                    return HttpResponseRedirect('/settings/account/')
                else:
                    return HttpResponse("New and Confirm passwords didn't match")
            else:
                return HttpResponse("You've typed wrong existing password")
            return HttpResponseRedirect('/settings/account/')
        else:
            return HttpResponseRedirect('/settings/account/')
    else:
        return HttpResponseRedirect('/login/')


@csrf_exempt
def remove_friend(request, username=None):
    if request.user.is_authenticated and request.method == 'POST':
        if username == None or username == request.user.username:
            return HttpResponseRedirect('/profile/')
        elif User.objects.filter(username=username).exists():
            friend_user = User.objects.get(username=username)
            user = User.objects.filter(username=request.user.username)
            Friend.objects.remove_friend(request.user, friend_user)
            return HttpResponseRedirect('/profile/' + username + '/')
        else:
            return HttpResponseRedirect('/profile/')
    else:
        return HttpResponseRedirect('/profile/')

def upgrade(request):
    if request.user.is_authenticated:
        userprofile = UserProfileInfo.objects.get(user=request.user)
        if userprofile.user_type != "Commercial":
            return render(request, 'Wallet/userUpgrade.html',{'userprofile':userprofile})
        else:
            return HttpResponseRedirect('/timeline/')
    else:
        return HttpResponseRedirect('/login/')

def validate_reset_email(request):
    if request.user.is_authenticated:
        email = request.GET.get('email', None)
        if User.objects.filter(email__iexact=email).exists():
            requser = User.objects.get(email__iexact=email)
            if requser == request.user:
                return HttpResponse(False)
            else:
                return HttpResponse(True)
        else:
            return HttpResponse(False)
    else:
        return HttpResponseRedirect('/login/')