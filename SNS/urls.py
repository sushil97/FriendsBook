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
import login
import signup
import user_account
from user_account import views
from SNS import settings
from signup import views
from login import views
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', signup.views.index, name='index'),
    url(r'^special/$', login.views.special, name='special'),
    url(r'^signup/$', signup.views.register, name="signup"),
    url(r'^login/$', login.views.user_login, name="login"),
    url(r'^profile/$',user_account.views.my_account,name='profile'),
    url(r'^settings/', include('django_mfa.urls'), name="mfa"),
    url(r'^timeline/$', user_account.views.my_timeline, name='timeline'),
    url(r'^logout/$', login.views.user_logout, name='logout'),
    url(r'^update_profile_pic/$', user_account.views.update_profile_pic, name='update_profile_pic'),
    url(r'^update_bio/$', user_account.views.update_bio, name='update_bio'),
    url(r'^search/$', user_account.views.search, name='search')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    #urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_DIR)
