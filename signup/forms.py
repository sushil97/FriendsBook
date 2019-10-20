from django import forms
from signup.models import UserProfileInfo
from django.contrib.auth.models import User

GENDER_CHOICES = [('Male', 'Male'),
                  ('Female', 'Female')]

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name',)


class UserProfileInfoForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect())

    class Meta():
        model = UserProfileInfo
        fields = ('profile_pic', 'dob', 'gender',)
