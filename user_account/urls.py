from django.conf.urls import url
from login import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'user_account'

urlpatterns=[

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)