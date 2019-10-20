import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from user_account.models import Post
from user_account.forms import PostForm
from user_account.forms import PrivacyInfoForm
from friendship.exceptions import AlreadyExistsError
from django.conf import settings
from signup.models import UserProfileInfo
from friendship.models import Friend, Follow, Block, FriendshipRequest

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

@csrf_exempt
def my_timeline(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        user_profile = UserProfileInfo.objects.get(user_id=user.id)
        friends_list = Friend.objects.friends(request.user)
        print(friends_list)
        friend_users=[]
        friend_users=friends_list.copy() #copy to prevent the change of list of friends
        friend_users.insert(0,user)
        print(friend_users)
        print(friends_list)
        # for i in friends_list:
        #     friend_users = User.objects.filter(Q(username=i))
        # print(friend_users)
        # original_user = User.objects.filter(id=request.user.id)
        #
        # print(friend_user_list)
        # for j in friend_user_list:
        #     friendship_ids.append(j.id)
        # print(friendship_ids)
        # friendship_ids.append(request.user.id)
        # print(friendship_ids)
        # for i in friendship_ids:
        #     posts_list = Post.objects.filter(Q(author_id=i)).order_by('created_date')
        # print(posts_list)
        # for i in posts_list:
        #     posts_ids.append(i.author_id)
        # print(posts_ids)
        # for i in posts_ids:
        #     posts_user = User.objects.filter(Q(id=i))
        # print(posts_user)
        # for friend_user in friend_user_list:
        #     friend_id=friend_user.id
        posts_list=Post.objects.all().order_by('-created_date')
        print(posts_list)
        context ={
            'user': user,
            'user_profile': user_profile,
            'friends_list':friends_list,
            'post_lists':posts_list,
            'friend_users':friend_users
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

@csrf_exempt
def privacy_info(request):
    user = request.user
    obj = get_object_or_404(UserProfileInfo, user_id=user.id)

    if request.user.is_authenticated:
        privacy_form = PrivacyInfoForm(request.POST,instance=obj)
        print(privacy_form.is_valid())
        if privacy_form.is_valid() and request.method == 'POST':
            obj = privacy_form.save(commit=False)
            obj.save()
        else:
            print(privacy_form.errors)
    else:
        privacy_form = PrivacyInfoForm()
    return render(request, 'settings/privacy.html')

def search(request):
    if request.user.is_authenticated and request.method == 'GET':
        user = request.user
        query = request.GET.get('search')
        users_list = User.objects.filter(Q(username=query) | Q(email=query))
        users_info_list=[]
        for i in users_list:
            userid = i.id
            users_info_list = UserProfileInfo.objects.filter(Q(user_id=userid))
        context={
            'user':user,
            'this_user_list': users_list,
            'this_user_profile_list':users_info_list,
            'query':query
        }
        return render_to_response('profile/search.html',context)
    else:
        return HttpResponseRedirect('/login')


@csrf_exempt
def create_post(request):
    user=request.user
    if request.method == 'POST':
        post_form = PostForm(data=request.POST)
        print(post_form)
        if user.is_authenticated:
            post_form = PostForm(data=request.POST)
            print(post_form)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.author=user
                post.save()
            else:
                print(post_form.errors)
        else:
            return HttpResponseRedirect("/login/")
    return HttpResponseRedirect("/timeline/")


def accountsettings(request):
    if request.user.is_authenticated:
        return render(request,'settings/account_settings.html')
    else:
        return HttpResponseRedirect('/timeline/')




# @csrf_exempt
# def add_friend(
#     request, to_username, template_name="friendship/friend/add.html"
# ):
#     """ Create a FriendshipRequest """
#     ctx = {"to_username": to_username}
#
#     if request.method == "POST":
#         to_user = User.objects.get(username=to_username)
#         from_user = request.user
#         try:
#             Friend.objects.add_friend(from_user, to_user)
#         except AlreadyExistsError as e:
#             ctx["errors"] = ["%s" % e]
#         else:
#             return redirect("friendship_request_list")
#
#     return render(request, template_name, ctx)
#
# def friend_requestlist(request):
#     if request.user.is_authenticated:
#         req_list = Friend.objects.unread_requests(user=request.user)
#         context={
#             'user':request.user,
#             'req_list': req_list
#         }
#         return render_to_response('profile/requests_list.html',context)
#     else:
#         return HttpResponseRedirect('/login/')
#
# def friendship_requests_detail(
#     request, friendship_request_id, template_name="friendship/friend/request.html"
# ):
#     """ View a particular friendship request """
#     f_request = get_object_or_404(FriendshipRequest, id=friendship_request_id)
#
#     return render(request, template_name, {"friendship_request": f_request})












# def add_friend(
#     request, to_username, template_name="profile/random_profile.html"
# ):
#     """ Create a FriendshipRequest """
#     ctx = {"to_username": to_username}
#
#     if request.method == "POST":
#         to_user = User.objects.get(username=to_username)
#         from_user = request.user
#         ctx ={
#             'user': to_user,
#         }
#         try:
#             Friend.objects.add_friend(from_user, to_user)
#         except AlreadyExistsError as e:
#             ctx["errors"] = ["%s" % e]
#         else:
#             return redirect("request_list")
#     return render(request, template_name, ctx)
