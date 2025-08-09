from enum import unique

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from social.storage_backends import ProfileImageStorage


class UserProfile(models.Model):
    options = (
        ("male",("Male")),
        ("female",("Female")),
    )
    userName = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    gender = models.CharField(max_length=20,choices=options,default="male",null=False,blank=False)
    dob = models.DateField(null=True,blank=True,default=None)
    bio = models.TextField(blank=True,null=True)
    phone = models.CharField(max_length=20,null=True,blank=True)
    profileImage = models.ImageField(storage=ProfileImageStorage(),upload_to="profile_image",null=True,blank=True)
    is_online = models.BooleanField(default=False)
    last_activity = models.DateTimeField(auto_now=True)
    fcm_token = models.CharField(max_length=255,blank=True,null=True,unique=True)

    def __str__(self):
        return f"{self.userName.username}"

    @property
    def is_active(self):
        from django.utils import timezone
        return self.is_online or (timezone.now() - self.last_activity).seconds < 300

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.get_or_create(userName=instance)


