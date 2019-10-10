from django.conf.urls import url
from django.conf.urls.static import static

from signup import views
from django.conf import settings

# SET THE NAMESPACE!
app_name = 'signup'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns = [
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    #urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)