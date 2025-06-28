from django.db import models
from django.contrib.auth.models import User

from comments.models import Comment
from posts.models import Post
from votes.models import Like
# Create your models here.

class Notification(models.Model):
    NOTIFICATION_TYPE = (
        ('like','Like'),
        ('comment','Comment',),
        ('reply','Reply'),
        ('comment_like','Comment like')
    )
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name="sent_notifications")
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name="receiver_notifications")
    post = models.ForeignKey(Post,on_delete=models.CASCADE,null=True,blank=True)
    like = models.ForeignKey(Like,on_delete=models.CASCADE,null=True,blank=True)
    notification_type = models.CharField(max_length=15,choices=NOTIFICATION_TYPE)
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,null=True,blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.sender} -> {self.receiver}:{self.notification_type}"