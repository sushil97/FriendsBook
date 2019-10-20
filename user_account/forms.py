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

PRIVACY_CHOICES = [('Me', 'Me'),
                  ('Friends', 'Friends'),
                   ('Everyone', 'Everyone')]

POST_PRIVACY_CHOICES = [('Friends', 'Friends'),
                   ('Everyone', 'Everyone')]


class PrivacyInfoForm(forms.ModelForm):
    privacy_email = forms.ChoiceField(choices=PRIVACY_CHOICES, widget=forms.RadioSelect())
    privacy_dob = forms.ChoiceField(choices=PRIVACY_CHOICES, widget=forms.RadioSelect())
    privacy_phone = forms.ChoiceField(choices=PRIVACY_CHOICES, widget=forms.RadioSelect())
    privacy_posts = forms.ChoiceField(choices=POST_PRIVACY_CHOICES, widget=forms.RadioSelect())

    class Meta():
        model = UserProfileInfo
        fields = ('privacy_email', 'privacy_dob', 'privacy_phone','privacy_posts',)