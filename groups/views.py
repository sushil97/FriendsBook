import datetime

from django.contrib.auth.models import Group, Permission, User
from django.core.mail import EmailMessage
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from groups.forms import GroupForm, GroupProfileInfoForm, GroupProfilePicUpdateForm, GroupRequestInfoForm, \
    GroupPostForm, GroupProfileUpdateForm, GroupInvitationInfoForm
from groups.models import GroupProfileInfo, GroupRequestInfo, GroupPost, GroupInvitation
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.http import JsonResponse
from signup.models import UserProfileInfo
from wallet.views import username, amount


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
        if GroupRequestInfo.objects.filter(from_user_id=request.user.id, to_admin_id=admin.id,
                                           group_id=group.id).exists():
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
                requester = UserProfileInfo.objects.get(user=request.user)
                admin = User.objects.get(id=groupprofileinfo.admin_id)
                from_user = request.user
                print(admin)
                print(from_user)
                group_request = group_request_form.save(commit=False)
                group_request.created = datetime.datetime.now()
                group_request.from_user = from_user
                # print(group_request.from_user)
                group_request.to_admin = admin
                group_request.group = group
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
            GroupRequestInfo.objects.filter(from_user_id=request.user.id, to_admin_id=admin.id,
                                            group_id=group.id).delete()

        return HttpResponseRedirect('/group_profile/' + name + '/')
    else:
        return HttpResponseRedirect('/login/')


@csrf_exempt
def group_invite(request):
    name = request.POST.get('name')
    group = Group.objects.get(name=name)
    groupprofileinfo = GroupProfileInfo.objects.get(group=group.id)
    admin = User.objects.get(id=groupprofileinfo.admin_id)
    username = request.POST.get('username', None)
    if request.user.is_authenticated:
        if request.method == 'POST' and request.user == admin:
            if User.objects.filter(username=username).exists():
                to_user = User.objects.get(username=username)
                if to_user in group.user_set.all():
                    return HttpResponse('user_exist')
                group_invite_form = GroupInvitationInfoForm(data=request.POST)
                if group_invite_form.is_valid():
                    if not GroupInvitation.objects.filter(to_user=to_user, from_admin=admin, group=group).exists():
                        print(groupprofileinfo)
                        print(admin)
                        print(to_user)
                        group_invite = group_invite_form.save(commit=False)
                        group_invite.to_user = to_user
                        group_invite.from_admin = admin
                        group_invite.group = group
                        group_invite.save()
                    else:
                        return HttpResponse('already_sent')
                else:
                    print(group_invite_form.errors)
            else:
                return HttpResponse('username_error')
            return HttpResponse('invitation_sent')
        else:
            group_invite_form = GroupInvitationInfoForm()
    else:
        return HttpResponseRedirect('/login/')


@csrf_exempt
def view_group_requests(request, name=None):
    group = Group.objects.get(name=name)
    groupprofileinfo = GroupProfileInfo.objects.get(group=group.id)
    admin = User.objects.get(id=groupprofileinfo.admin_id)
    if request.user.is_authenticated:
        if request.user == admin:
            group_requests = GroupRequestInfo.objects.filter(to_admin_id=request.user.id, group_id=group.id)
            context = {
                'group_requests': group_requests
            }
            return render(request, 'groups/group_request.html', context)
        else:
            return HttpResponseRedirect('/timeline/')
    else:
        return HttpResponseRedirect('/login/')


@csrf_exempt
def group_requests_detail(request, name=None, username=None):
    group = Group.objects.get(name=name)
    user = User.objects.get(username=username)
    groupprofileinfo = GroupProfileInfo.objects.get(group=group.id)
    admin = User.objects.get(id=groupprofileinfo.admin_id)
    if request.user.is_authenticated:
        if request.user == admin:
            g_request = get_object_or_404(GroupRequestInfo, from_user=user, group=group)
            return render(request, 'groups/group_request_view.html', {"group_request": g_request})
        else:
            return HttpResponseRedirect('/timeline/')
    else:
        return HttpResponseRedirect('/login/')


@csrf_exempt
def group_request_accept(request, name=None, username=None):
    group = Group.objects.get(name=name)
    user = User.objects.get(username=username)
    groupprofileinfo = GroupProfileInfo.objects.get(group=group.id)
    admin = User.objects.get(id=groupprofileinfo.admin_id)
    if request.user.is_authenticated:
        if request.user == admin:
            if request.method == "POST":
                GroupRequestInfo.objects.filter(to_admin=request.user, from_user=user, group=group).delete()
                group.user_set.add(user)
                # make perfect response page after accepting the request
                # make webpage for showing members of the group
                return HttpResponseRedirect('/show_group_members/' + name + '/')
            return HttpResponseRedirect('/show_group_members/' + name + '/')
        else:
            return HttpResponseRedirect('/timeline/')
    else:
        return HttpResponseRedirect('/login/')


@csrf_exempt
def group_request_reject(request, name=None, username=None):
    group = Group.objects.get(name=name)
    user = User.objects.get(username=username)
    groupprofileinfo = GroupProfileInfo.objects.get(group=group.id)
    admin = User.objects.get(id=groupprofileinfo.admin_id)
    if request.user.is_authenticated:
        if request.user == admin:
            # obj = get_object_or_404(GroupRequestInfo, from_user=user, group=group)
            # group_request_form = GroupRequestInfoForm(data=request.POST, instance=obj)
            # if request.method == 'POST' and group_request_form.is_valid():
            #     group_request = group_request_form.save(commit=False)
            #     group_request.rejected = timezone.now()
            #     group_request.save()
            GroupRequestInfo.objects.filter(from_user=user, to_admin=admin, group=group).delete()
            return HttpResponseRedirect('/show_group_members/' + name + '/')
        else:
            return HttpResponseRedirect('/timeline/')
    else:
        return HttpResponseRedirect('/login/')


@csrf_exempt
def show_group_members(request, name=None):
    user = request.user
    admin_flag = False
    group = Group.objects.get(name=name)
    groupprofileinfo = GroupProfileInfo.objects.get(group=group.id)
    admin = User.objects.get(id=groupprofileinfo.admin_id)
    if request.user.is_authenticated:
        members = group.user_set.all().order_by('username')
        if user == admin:
            admin_flag = True
        context = {
            'user': user,
            'admin': admin,
            'group': group,
            'members': members,
            'admin_flag': admin_flag
        }
        return render_to_response('groups/user_list.html', context)
    else:
        return HttpResponseRedirect('/login/')


@csrf_exempt
def group_timeline(request, name=None):
    user = request.user
    group = Group.objects.get(name=name)
    groupprofileinfo = GroupProfileInfo.objects.get(group=group.id)
    group_posts = GroupPost.objects.filter(group=group.id).order_by('-created_date')
    admin = User.objects.get(id=groupprofileinfo.admin_id)
    admin_flag = False
    if user.is_authenticated:
        if user in group.user_set.all():
            members = group.user_set.all().order_by('username')
            if request.user == admin:
                admin_flag = True
            context = {
                'group': group,
                'group_profile': groupprofileinfo,
                'user': user,
                'members': members,
                'group_posts': group_posts,
                'admin_flag': admin_flag
            }
            return render_to_response('groups/group_timeline.html', context)
        else:
            return HttpResponseRedirect('/timeline/')
    else:
        return HttpResponseRedirect('/login/')


@csrf_exempt
def remove_group_member(request, name=None, username=None):
    user = User.objects.get(username=username)
    group = Group.objects.get(name=name)
    groupprofileinfo = GroupProfileInfo.objects.get(group=group.id)
    admin = User.objects.get(id=groupprofileinfo.admin_id)
    if request.user.is_authenticated:
        if request.user == admin:
            group.user_set.remove(user)
            return HttpResponseRedirect('/show_group_members/' + name + '/')
        else:
            return HttpResponseRedirect('/group_profile/' + name + '/')
    else:
        return HttpResponseRedirect('/login/')


@csrf_exempt
def create_group_post(request, name=None, username=None):
    user = request.user
    group = Group.objects.get(name=name)
    if user.is_authenticated:
        if user in group.user_set.all():
            if request.method == 'POST':
                post_form = GroupPostForm(data=request.POST)
                if post_form.is_valid():
                    post = post_form.save(commit=False)
                    post.author = user
                    post.group = group
                    post.save()
                    return HttpResponseRedirect('/group_timeline/' + name + '/')
                else:
                    print(post_form.errors)
            else:
                return HttpResponseRedirect('/group_timeline/' + name + '/')
        else:
            return HttpResponseRedirect('/timeline/')
    else:
        return HttpResponseRedirect('/login/')


@csrf_exempt
def view_invitations(request):
    # groups = request.user.groups.values_list('name', flat=True)  # QuerySet Object
    if request.user.is_authenticated:
        invitations = GroupInvitation.objects.filter(to_user=request.user).order_by('created')
        print(invitations)
        context = {
            'invitations': invitations
        }
        return render(request, 'groups/group_invitation_request.html', context)
    else:
        return HttpResponseRedirect('/login/')


@csrf_exempt
def invitation_detail(request, name=None):
    group = Group.objects.get(name=name)
    if request.user.is_authenticated:
        return render(request, 'groups/group_invtitation_request_view.html', {"group": group})
    else:
        return HttpResponseRedirect('/login/')


@csrf_exempt
def accept_invitation(request, name=None):
    if request.user.is_authenticated and request.method == 'POST':
        group = Group.objects.get(name=name)
        GroupInvitation.objects.filter(to_user=request.user, group=group).delete()
        group.user_set.add(request.user)
        return HttpResponseRedirect('/group_profile/' + name + '/')
    else:
        return HttpResponseRedirect('/login/')


@csrf_exempt
def reject_invitation(request, name=None):
    if request.user.is_authenticated:
        group = Group.objects.get(name=name)
        # obj = get_object_or_404(GroupInvitation, to_user=request.user, group=group)
        # invitation_form = GroupInvitationInfoForm(data=request.POST, instance=obj)
        # if request.method == 'POST' and invitation_form.is_valid():
        #     invitation_request = invitation_form.save(commit=False)
        #     invitation_request.rejected = timezone.now()
        #     invitation_request.save()
        GroupInvitation.objects.filter(to_user=request.user, group=group).delete()
        return HttpResponseRedirect('/group_profile/' + name + '/')
    else:
        return HttpResponseRedirect('/login/')


@csrf_exempt
def delete_group(request, name=None):
    group = Group.objects.get(name=name)
    groupprofileinfo = GroupProfileInfo.objects.get(group=group.id)
    admin = User.objects.get(id=groupprofileinfo.admin_id)
    if request.user.is_authenticated:
        if request.user == admin:
            group.delete()
            return HttpResponseRedirect('/timeline/')
        else:
            return HttpResponseRedirect('/timeline/')
    else:
        return HttpResponseRedirect('/login/')


@csrf_exempt
def leave_group(request, name=None):
    group = Group.objects.get(name=name)
    groupprofileinfo = GroupProfileInfo.objects.get(group=group.id)
    admin = User.objects.get(id=groupprofileinfo.admin_id)
    if request.user.is_authenticated:
        if request.method == 'POST' and group.user_set.filter(
                username=request.user.username).exists() and request.user != admin:
            group.user_set.remove(request.user)
            return HttpResponseRedirect('/timeline/')
        else:
            return HttpResponseRedirect('/timeline/')
    else:
        return HttpResponseRedirect('/login/')


@csrf_exempt
def update_group_bio(request, name=None):
    group = Group.objects.get(name=name)
    groupprofileinfo = GroupProfileInfo.objects.get(group=group.id)
    admin = User.objects.get(id=groupprofileinfo.admin_id)
    obj = get_object_or_404(GroupProfileInfo, group=group.id)
    if request.user.is_authenticated:
        bio_form = GroupProfileUpdateForm(request.POST, instance=obj)
        if request.method == 'POST' and bio_form.is_valid() and request.user == admin:
            obj = bio_form.save(commit=False)
            obj.save()
        return HttpResponseRedirect('/group_profile/' + name + '/')
    return HttpResponseRedirect('/login/')


@csrf_exempt
def update_group_profile_pic(request, name=None):
    user = request.user
    default = 'default_pic/default_pic.jpg'
    if request.user.is_authenticated:
        group = Group.objects.get(name=name)
        image_form = GroupProfilePicUpdateForm(request.POST, request.FILES)
        if request.method == 'POST' and image_form.is_valid():
            profile = GroupProfileInfo.objects.get(group=group.id)
            if profile.group_pic == default:
                profile.group_pic = image_form.cleaned_data['group_pic']
                profile.save()
            else:
                profile.group_pic.delete(False)
                profile.group_pic = image_form.cleaned_data['group_pic']
                profile.save()
        return HttpResponseRedirect('/group_profile/' + name + '/')
    return HttpResponseRedirect('/login/')


@csrf_exempt
def validate_groupname(request):
    name = request.GET.get('name', None)
    if Group.objects.filter(name__iexact=name).exists():
        print("Username NOT available")
        return HttpResponse(True)
    else:
        print("Username Available")
        return HttpResponse(False)
