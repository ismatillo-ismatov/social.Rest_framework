from django.db import models
from posts.models import Post


class Like(models.Model):
    post = models.ForeignKey(Post,related_name="votes",on_delete=models.CASCADE)
    user = models.ForeignKey("auth.User",related_name='likes',on_delete=models.CASCADE,default=None,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post','user')

    def __str__(self):
        return self.post.content


    