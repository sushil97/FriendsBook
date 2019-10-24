from django.conf.urls import url
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

app_name = 'groups'

urlpatterns=[

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)