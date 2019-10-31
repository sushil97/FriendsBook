from django import forms
from groups.models import GroupProfileInfo, GroupRequestInfo, GroupPost, GroupInvitation
from django.contrib.auth.models import Group


class GroupForm(forms.ModelForm):
    class Meta():
        model = Group
        fields = ('name',)

class GroupProfileInfoForm(forms.ModelForm):

    class Meta():
        model = GroupProfileInfo
        fields = ('group_pic', 'biography','fee',)

class GroupProfilePicUpdateForm(forms.ModelForm):
    group_pic = forms.ImageField()

    class Meta:
        model = GroupProfileInfo
        fields = ('group_pic',)

class GroupProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = GroupProfileInfo
        fields = ('biography','fee')

class GroupRequestInfoForm(forms.ModelForm):
    class Meta:
        model = GroupRequestInfo
        fields =()

class GroupInvitationInfoForm(forms.ModelForm):
    class Meta:
        model = GroupInvitation
        fields =()

class GroupPostForm(forms.ModelForm):
    class Meta:
        model = GroupPost
        fields = ('title', 'text')