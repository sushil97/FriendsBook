from django.contrib.auth.models import Group, Permission
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def create_group(request):
    user = request.user
    if request.user.is_authenticated:
        if request.method == 'POST':
            group_name = request.POST['group_name']
            if Group.objects.filter(name=group_name).exists():
                # group = Group.objects.get(name=group_name)
                # group.user_set.add(user)
                return HttpResponse('Group Already Exists')
            else:
                group, created = Group.objects.get_or_create(name=group_name)
                group.user_set.add(user)
                # perm1 = Permission.objects.get(name='Can change group')
                # perm2 = Permission.objects.get(name='Can delete group')
                # user.user_permissions.add(perm1, perm2)
                return HttpResponse(True)
    return HttpResponse(False)
