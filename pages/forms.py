from django import forms
from pages.models import PagePost, PageProfileInfo, PageFollowInfo

class PageProfileInfoForm(forms.ModelForm):
    class Meta():
        model = PageProfileInfo
        fields = ('page', 'page_pic','biography',)


class PageProfilePicUpdateForm(forms.ModelForm):
    page_pic = forms.ImageField()

    class Meta:
        model = PageProfileInfo
        fields = ('page_pic',)

class PageUpdateForm(forms.ModelForm):

    class Meta:
        model = PageProfileInfo
        fields = ('biography',)

class PageFollowInfoForm(forms.ModelForm):
    class Meta:
        model = PageFollowInfo
        fields =()

class PageUnFollowInfoForm(forms.ModelForm):
    class Meta:
        model = PageFollowInfo
        fields =()

class PagePostForm(forms.ModelForm):
    class Meta:
        model = PagePost
        fields = ('title', 'text',)