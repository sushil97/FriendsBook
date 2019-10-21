from django.db import models
from django.utils import timezone
from django.conf import settings

AUTH_USER_MODEL = getattr(settings, "AUTH_USER_MODEL", "auth.User")

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE)
    receiver = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='receiver_name',null=True)
    title = models.CharField(max_length=200)
    text = models.TextField(blank=False, null=False)
    created_date = models.DateTimeField(
            default=timezone.now)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title