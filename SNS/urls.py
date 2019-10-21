"""SNS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.contrib.sites.models import Site
import login
import signup
import user_account
import django_mfa
from user_account import views
from SNS import settings
from signup import views
from login import views
from django.contrib.staticfiles.urls import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', signup.views.index, name='index'),
    url(r'^special/$', login.views.special, name='special'),
    url(r'^signup/$', signup.views.register, name="signup"),
    url(r'^login/$', login.views.user_login, name="login"),
    url(r'^profile/$',user_account.views.my_account,name='profile'),
    url(r'^profile/(?P<username>.+)/$', login.views.show_profile, name="show_profile"),
    url(r'^create_post/(?P<username>.+)/$', user_account.views.create_profile_post, name="save_profile_post"),
    url(r'^friendship/', include('friendship.urls')),
    url(r'^settings/', include('django_mfa.urls'), name="mfa"),
    url(r'^timeline/$', user_account.views.my_timeline, name='timeline'),
    url(r'^logout/$', login.views.user_logout, name='logout'),
    url(r'^update_profile_pic/$', user_account.views.update_profile_pic, name='update_profile_pic'),
    url(r'^update_bio/$', user_account.views.update_bio, name='update_bio'),
    url(r'^search/$', user_account.views.search, name='search'),
    # url(r"^friends/(?P<username>[\w-]+)/$",user_account.views.view_friends,"friendship_view_friends"),
    # url(r"^add/(?P<to_username>[\w-]+)/$",user_account.views.add_friend, name="add_friend"),
    # url(r"^friend/requests/$",user_account.views.friend_requestlist,name="friend_requestlist"),
    url(r'^validate_username/$', signup.views.validate_username, name='validate_username'),
    url(r'^create_post/$',user_account.views.create_post,name='create_post'),
    url(r'^settings/account/$',user_account.views.accountsettings, name="accountsettings"),
    url(r'^messages/', include('django_messages.urls')),
    url(r'^settings/privacy/$',user_account.views.privacy_info, name='privacy_info'),
    url(r'^remove_friend/(?P<username>.+)/$',user_account.views.remove_friend, name='remove_friend')
    # url(r"^friend/request/(?P<friendship_request_id>\d+)/$",user_account.views.friendship_requests_detail,name="friendship_requests_detail")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    #urlpatterns += static(setting.STATIC_URL, document_root=setting.STATIC_ROOT)
    # urlpatterns += static(setting.MEDIA_URL, document_root=setting.MEDIA_DIR)
