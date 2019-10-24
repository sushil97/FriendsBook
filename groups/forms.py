from django import forms
from groups.models import GroupProfileInfo, GroupRequestInfo, GroupPost
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

class GroupRequestInfoForm(forms.ModelForm):
    class Meta:
        model = GroupRequestInfo
        fields =()

class GroupPostForm(forms.ModelForm):
    class Meta:
        model = GroupPost
        fields = ('title', 'text')