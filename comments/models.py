from django.db import models
from posts.models import Post
import datetime


class Comment(models.Model):
    owner = models.ForeignKey("auth.User",on_delete=models.CASCADE)
    post = models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
    parent = models.ForeignKey("self",on_delete=models.CASCADE, null=True,blank=True, related_name="replies",)
    comment = models.CharField(max_length=4000)
    comment_image = models.ImageField(upload_to="comment_image",blank=True,null=True)
    comment_date = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField("auth.User",related_name='liked_comments',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.comment

    @property
    def like_count(self):
        return self.likes.count()
