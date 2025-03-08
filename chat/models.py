from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from user_profile.models import UserProfile


def default_userprofile():
    profile = UserProfile.objects.first()
    if not profile:
        user = User.objects.create_user(username='default_user',password='temp_password')
        profile = UserProfile.objects.create(user=user)
    return profile



class Message(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="sender",null=False,default=default_userprofile)
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="receiver",null=False,default=default_userprofile)
    # sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name="sender")
    # receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name="receiver")
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message
    class Meta:
        ordering = ("timestamp",)

# def post_user_massage_signal(sender,instance,created,**kwargs):
#     if created:
#         Message.objects.create(user=instance)
#
# post_save.connect(post_user_massage_signal,sender=User)