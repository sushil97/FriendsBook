from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from pages.models import PageProfileInfo, PagePost, PageFollowInfo
from pages.forms import PageProfileInfoForm, PagePostForm, PageUpdateForm, PageProfilePicUpdateForm, PageUnFollowInfoForm, PageFollowInfoForm


# Create your views here.
from signup.models import UserProfileInfo


def create_page(request):
    created = False
    user = request.user
    if request.user.is_authenticated:
        userprofile = UserProfileInfo.objects.get(user=request.user)
        if userprofile.user_type=="Commercial":
            if request.method == 'POST':
                page_name = request.POST.get('page')
                page_profile_form = PageProfileInfoForm(data=request.POST)
                if page_profile_form.is_valid():
                    page_profile = page_profile_form.save(commit=False)
                    page_profile.admin = request.user
                    if 'page_pic' in request.FILES:
                        page_profile.page_pic = request.FILES['page_pic']
                    page_profile.save()
                    created = True
                else:
                    print(page_profile_form.errors)
            else:
                page_profile_form = PageProfileInfoForm()
            return render(request, 'pages/create_page.html', {'created': created,'page_name':page_name})
        else:
            return HttpResponseRedirect('/timeline/')
    else:
        return HttpResponseRedirect('/login/')


def page_timeline(request, page=None):
    user = request.user
    pages = PageProfileInfo.objects.get(page=page)
    posts = PagePost.objects.filter(page=page).order_by('-created_date')
    follower_status=False
    if user.is_authenticated:
        admin_status=False
        if request.user == pages.admin:
            admin_status=True
        if PageFollowInfo.objects.filter(from_user=user,page=pages).exists():
            follower_status=True
        context = {
            'user':user,
            'admin_status':admin_status,
            'pages':pages,
            'posts':posts,
            'follower_status':follower_status
        }
        return render_to_response('pages/page_timeline.html', context)
    else:
        return HttpResponseRedirect('/login/')


@csrf_exempt
def create_page_post(request, page=None):
    user = request.user
    pages = PageProfileInfo.objects.get(page=page)
    if user.is_authenticated:
        if user==pages.admin and request.method=='POST':
            post_form = PagePostForm(data=request.POST)
            print(request.FILES)
            print(post_form)
            print(post_form.is_valid())
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.author=user
                post.page=pages
                if 'post_pic' in request.FILES:
                    print('Yes')
                    post.post_pic = request.FILES['post_pic']
                post.save()
            else:
                post_form = PagePostForm()
            return HttpResponseRedirect('/page_timeline/'+page+'/')
        else:
            return HttpResponseRedirect('/page_timeline/'+page+'/')
    else:
        return HttpResponseRedirect('/login/')


@csrf_exempt
def follow_page(request,page=None):
    if request.user.is_authenticated:
        pages = PageProfileInfo.objects.get(page=page)
        if pages.admin != request.user:
            if request.method=='POST':
                follow_form = PageFollowInfoForm(request.POST)
                if follow_form.is_valid():
                    follow = follow_form.save(commit=False)
                    follow.from_user = request.user
                    follow.page = pages
                    follow.save()
                    return HttpResponseRedirect('/page_timeline/' + page + '/')
            else:
                return HttpResponseRedirect('/page_timeline/'+page+'/')
        else:
            return HttpResponseRedirect('/page_timeline/'+page+'/')
    else:
        return HttpResponseRedirect('/login/')

@csrf_exempt
def unfollow_page(request,page=None):
    if request.user.is_authenticated:
        pages = PageProfileInfo.objects.get(page=page)
        if pages.admin != request.user:
            if request.method=='POST':
                follow_form = PageUnFollowInfoForm(request.POST)
                if follow_form.is_valid():
                    PageFollowInfo.objects.filter(from_user=request.user,page=pages).delete()
                    return HttpResponseRedirect('/page_timeline/' + page + '/')
            else:
                return HttpResponseRedirect('/page_timeline/'+page+'/')
        else:
            return HttpResponseRedirect('/page_timeline/' + page + '/')
    else:
        return HttpResponseRedirect('/login/')

@csrf_exempt
def validate_pagename(request):
    page = request.GET.get('page', None)
    if PageProfileInfo.objects.filter(page__iexact=page).exists():
        print("Username NOT available")
        return HttpResponse(True)
    else:
        print("Username Available")
        return HttpResponse(False)

def launch_create_page(request):
    if request.user.is_authenticated:
        user_profile = UserProfileInfo.objects.get(user=request.user)
        if user_profile.user_type=="Commercial":
            return render(request, 'pages/create_page.html')
        else:
            return HttpResponseRedirect('/timeline/')
    else:
        return HttpResponseRedirect('/login/')

@csrf_exempt
def update_page_pic(request,page=None):
    user = request.user
    pages = PageProfileInfo.objects.get(page=page)
    if request.user.is_authenticated:
        image_form = PageProfilePicUpdateForm(request.POST, request.FILES)
        print(image_form.is_valid())
        if user == pages.admin:
            if request.method == 'POST' and image_form.is_valid() :
                # profile = PageProfileInfo.objects.get(user_id=user.id)
                pages.page_pic.delete(False)
                pages.page_pic = image_form.cleaned_data['page_pic']
                pages.save()
            else:
                print(image_form.errors)
            return HttpResponseRedirect('/page_timeline/'+page+'/')
        else:
            return HttpResponseRedirect('/page_timeline/'+page+'/')
    else:
        return HttpResponseRedirect('/login/')


@csrf_exempt
def update_page_bio(request, page=None):
    user =request.user
    pages = PageProfileInfo.objects.get(page=page)
    obj = get_object_or_404(PageProfileInfo, page=page)
    if request.user.is_authenticated:
        bio_form = PageUpdateForm(request.POST, instance=obj)
        if user == pages.admin:
            if request.method == 'POST' and bio_form.is_valid():
                obj = bio_form.save(commit=False)
                obj.save()
            else:
                print(bio_form.errors)
            return HttpResponseRedirect('/page_timeline/' + page + '/')
        else:
            return HttpResponseRedirect('/page_timeline/'+page+'/')
    else:
        return HttpResponseRedirect('/login/')