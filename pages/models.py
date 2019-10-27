from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group, User

# Create your models here.
class PageProfileInfo(models.Model):
    page = models.CharField(max_length=30,null=False,blank=False,primary_key=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    page_pic = models.ImageField(upload_to='page_profile_pic/', default='group_profile_pics/logo.png', blank=True)
    biography = models.TextField(max_length=200, blank=False)

class PageFollowInfo(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitation_from')
    page = models.ForeignKey(PageProfileInfo,on_delete=models.CASCADE)

class PagePost(models.Model):
    page = models.ForeignKey(PageProfileInfo,on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField(blank=False, null=False)
    post_pic = models.ImageField(upload_to='page_post_pic/',blank=False,null=False)
    created_date = models.DateTimeField(
        default=timezone.now)

# class PageInvitation(models.Model):
#     page = models.ForeignKey(PageProfileInfo, on_delete=models.CASCADE)
#     to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='page_invitation_to')
#     from_admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='page_invitation_from')
#     created = models.DateTimeField(default=timezone.now)
#     rejected = models.DateTimeField(blank=True, null=True)

