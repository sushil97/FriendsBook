from django.db import models
from django.contrib.auth.models import User
from signup.models import UserProfileInfo


# Create your models here.
class Transaction(models.Model):
    sender = models.ForeignKey(User, null=False, max_length=20, on_delete=models.CASCADE, related_name="sender_user")
    receiver = models.ForeignKey(User ,null=True, blank=True,max_length=20, on_delete=models.CASCADE, related_name="receiver_user")
    amount = models.IntegerField(null=False)
    trans_id = models.IntegerField(unique=True,null=False)

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    otp = models.IntegerField(null=False)

def __str__(self):
    return self.user.username
