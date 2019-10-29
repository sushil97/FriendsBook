from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=False, default='1997-01-01')
    gender = models.CharField(max_length=10)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default_pic/default_pic.jpg', blank=True)
    biography = models.TextField(max_length=200, blank=True)
    country = models.CharField(max_length=50, blank=True)
    mobile = models.CharField(max_length=15, blank=True)
    privacy_email = models.CharField(max_length=10, default="Everyone")
    privacy_dob = models.CharField(max_length=10, default="Everyone")
    privacy_phone = models.CharField(max_length=10, default="Everyone")
    privacy_posts = models.CharField(max_length=10, default="Everyone")

def __str__(self):
    return self.user.username
