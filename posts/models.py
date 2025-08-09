from django.db import models
from django.contrib.auth.models import User
from social.storage_backends import PublicMediaStorage,VideoStorage



class Post(models.Model):
    owner = models.ForeignKey("auth.User",related_name="posts",on_delete=models.CASCADE)
    content = models.TextField()
    postImage = models.ImageField(upload_to="",storage=PublicMediaStorage(),null=True,blank=True)
    postVideo = models.FileField(upload_to="post_video",storage=VideoStorage(),null=True,blank=True)
    post_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.content

class Story(models.Model):
    owner = models.ForeignKey("auth.User",related_name='user',on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    story = models.FileField('stories',upload_to="media/story")
    story_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title



class StoryMessage(models.Model):
    sender = models.ForeignKey(User,related_name="sent_message",on_delete=models.CASCADE)
    recipient = models.ForeignKey(User,related_name='received_message',on_delete=models.CASCADE)
    story = models.ForeignKey(Story,on_delete=models.CASCADE)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

