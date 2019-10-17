from django import forms
from django.forms import ModelForm
from user_account.models import Post
from signup.models import UserProfileInfo

class ProfilePicUpdateForm(ModelForm):
    profile_pic = forms.ImageField()

    class Meta:
        model = UserProfileInfo
        fields = ('profile_pic',)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text')

class ProfileUpdateForm(ModelForm):
    biography = forms.TextInput()

    class Meta:
        model = UserProfileInfo
        fields = ('biography','country','mobile','dob')