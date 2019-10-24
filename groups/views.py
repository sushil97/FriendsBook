from django.contrib.auth.models import Group, Permission, User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from groups.forms import GroupForm, GroupProfileInfoForm, GroupProfilePicUpdateForm, GroupRequestInfoForm
from groups.models import GroupProfileInfo, GroupRequestInfo
from django.views.decorators.csrf import csrf_exempt
import datetime


@csrf_exempt
def create_group(request):
    created = False
    user = request.user
    if request.user.is_authenticated:
        if request.method == 'POST':
            group_name = request.POST['name']
            # group_form = GroupForm(data=request.POST)
            group_profile_form = GroupProfileInfoForm(data=request.POST)
            if group_profile_form.is_valid():
                group = Group.objects.create(name=group_name)
                group.user_set.add(user)
                group_profile = group_profile_form.save(commit=False)
                group_profile.group = group
                group_profile.admin = request.user
                if 'group_pic' in request.FILES:
                    group_profile.group_pic = request.FILES['group_pic']
                group_profile.save()
                created = True
            else:
                print(group_profile_form.errors)
        else:
            group_profile_form = GroupProfileInfoForm()
        return HttpResponseRedirect('/group_profile/' + group_name + '/')
        # return render(request, 'groups/group.html',{'created':created})
    else:
        return HttpResponseRedirect('/login/')

    #         group_name = request.POST['group_name']
    #         if Group.objects.filter(name=group_name).exists():
    #             # group = Group.objects.get(name=group_name)
    #             # group.user_set.add(user)
    #             return HttpResponse('Group Already Exists')
    #         else:
    #             group, created = Group.objects.get_or_create(name=group_name)
    #             group.user_set.add(user)
    #             # perm1 = Permission.objects.get(name='Can change group')
    #             # perm2 = Permission.objects.get(name='Can delete group')
    #             # user.user_permissions.add(perm1, perm2)
    #             return HttpResponse(True)
    # return HttpResponse(False)


def profile(request, name=None):
    user = request.user
    if request.user.is_authenticated and Group.objects.filter(name=name).exists():
        group = Group.objects.get(name=name)
        request_status = False
        groupprofileinfo = GroupProfileInfo.objects.get(group=group.id)
        group_members = group.user_set.all()
        admin = User.objects.get(id=groupprofileinfo.admin.id)
        if GroupRequestInfo.objects.filter(from_user_id=request.user.id, to_admin_id=admin.id).exists():
            request_status = True

        context = {
            'group_members': group_members,
            'user': user,
            'group': group,
            'admin': admin,
            'groupprofileinfo': groupprofileinfo,
            'request_status': request_status
        }
        return render_to_response('groups/group_profile.html', context)
    else:
        return HttpResponseRedirect('/login/')


def launch_create_group(request):
    if request.user.is_authenticated:
        return render(request, 'groups/group.html')
    else:
        return HttpResponseRedirect('/login/')


@csrf_exempt
def groups_requests(request, name=None):
    if request.user.is_authenticated:
        if request.method == 'POST':
            group_request_form = GroupRequestInfoForm(data=request.POST)
            group = Group.objects.get(name=name)
            if group_request_form.is_valid():
                groupprofileinfo = GroupProfileInfo.objects.get(group=group.id)
                print(groupprofileinfo)
                admin = User.objects.get(id=groupprofileinfo.admin_id)
                from_user = request.user
                print(admin)
                print(from_user)
                group_request = group_request_form.save(commit=False)
                # group_request.created = datetime.datetime.now()
                group_request.from_user = from_user
                # print(group_request.from_user)
                group_request.to_admin = admin
                group_request.save()
            else:
                print(group_request_form.errors)
        else:
            group_request_form = GroupRequestInfoForm()
        return HttpResponseRedirect('/group_profile/' + name + '/')
    else:
        return HttpResponseRedirect('/login/')


@csrf_exempt
def cancel_requests(request, name=None):
    if request.user.is_authenticated:
        if request.method == 'POST':
            group = Group.objects.get(name=name)
            groupprofileinfo = GroupProfileInfo.objects.get(group=group.id)
            admin = User.objects.get(id=groupprofileinfo.admin_id)
            GroupRequestInfo.objects.filter(from_user_id=request.user.id, to_admin_id=admin.id).delete()
        return HttpResponseRedirect('/group_profile/' + name + '/')
    else:
        return HttpResponseRedirect('/login/')


# def update_group_bio(request, name=None):
#     user = request.user
#     obj = get_object_or_404(UserProfileInfo,user_id=user.id)
#     if request.user.is_authenticated:
#         bio_form = ProfileUpdateForm(request.POST, instance=obj)
#         context={
#             'bio_form': bio_form
#         }
#         if request.method == 'POST' and bio_form.is_valid():
#             # profile = UserProfileInfo.objects.get(user_id=user.id)
#             obj=bio_form.save(commit=False)
#             obj.save()
#             # delattr(profile, 'biography')
#             # setattr(profile,'biography',bio_form)
#             # profile.save()
#         return HttpResponseRedirect('/profile/')
#     return HttpResponseRedirect('/login/')

@csrf_exempt
def update_group_profile_pic(request, name=None):
    user = request.user
    if request.user.is_authenticated:
        group = Group.objects.get(name=name)
        image_form = GroupProfilePicUpdateForm(request.POST, request.FILES)
        if request.method == 'POST' and image_form.is_valid():
            profile = GroupProfileInfo.objects.get(group=group.id)
            profile.group_pic.delete(False)
            profile.group_pic = image_form.cleaned_data['group_pic']
            profile.save()
        return HttpResponseRedirect('/group_profile/' + name + '/')
    return HttpResponseRedirect('/login/')
