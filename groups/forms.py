from django import forms
from groups.models import GroupProfileInfo, GroupRequestInfo, GroupPost, GroupInvitation
from django.contrib.auth.models import Group

TYPE_CHOICES = [('Public', 'Public'),
                  ('Private', 'Private')]

class GroupForm(forms.ModelForm):
    class Meta():
        model = Group
        fields = ('name',)

class GroupProfileInfoForm(forms.ModelForm):
    type = forms.ChoiceField(choices=TYPE_CHOICES, widget=forms.RadioSelect())

    class Meta():
        model = GroupProfileInfo
        fields = ('type', 'group_pic', 'biography','fee',)

class GroupProfilePicUpdateForm(forms.ModelForm):
    group_pic = forms.ImageField()

    class Meta:
        model = GroupProfileInfo
        fields = ('group_pic',)

class GroupProfileUpdateForm(forms.ModelForm):
    type = forms.ChoiceField(choices=TYPE_CHOICES, widget=forms.RadioSelect())

    class Meta:
        model = GroupProfileInfo
        fields = ('biography','type','fee')

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