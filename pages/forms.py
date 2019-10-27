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
#
# class GroupProfileUpdateForm(forms.ModelForm):
#     type = forms.ChoiceField(choices=TYPE_CHOICES, widget=forms.RadioSelect())
#
#     class Meta:
#         model = GroupProfileInfo
#         fields = ('biography','type','fee')
#
# class GroupRequestInfoForm(forms.ModelForm):
#     class Meta:
#         model = GroupRequestInfo
#         fields =()
#
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