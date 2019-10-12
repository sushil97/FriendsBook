from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=False, default='1997-01-01')
    gender = models.CharField(max_length=10)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='profile_pics/kishan.jpg', blank=True)
    biography = models.TextField(max_length=200, blank=True)

def __str__(self):
    return self.user.username
