from django import forms
from django.forms import ModelForm

from signup.models import UserProfileInfo

class ProfilePicUpdateForm(ModelForm):
    profile_pic = forms.ImageField()

    class Meta:
        model = UserProfileInfo
        fields = ('profile_pic',)

class BioUpdateForm(ModelForm):
    biography = forms.TextInput()

    class Meta:
        model = UserProfileInfo
        fields = ('biography',)