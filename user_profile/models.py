from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class UserProfile(models.Model):
    options = (
        ("male",("Male")),
        ("female",("Female")),
        ("others",("others")),
    )
    userName = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    gender = models.CharField(max_length=20,choices=options,default="male",null=False,blank=False)
    dob = models.DateField(null=True,blank=True,default=None)
    phone = models.CharField(max_length=20,null=True,blank=True)
    profileImage = models.ImageField(upload_to="profile_image",null=True,blank=True)

    def __str__(self):
        return f"{self.userName.username}"

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.get_or_create(userName=instance)


