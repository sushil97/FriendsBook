from django.conf.urls import url
from login import views
from django.conf.urls.static import static
from django.conf import settings

# SET THE NAMESPACE!
app_name = 'login'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns = [
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    #urlpatterns += static(setting.STATIC_URL, document_root=setting.STATIC_ROOT)