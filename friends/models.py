from datetime import datetime
from user_profile.models import UserProfile
from django.db import models


class FriendsRequest(models.Model):
    request_from = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="send_requests")
    request_to = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="received_request")
    status = models.CharField(max_length=50, choices=[('Pending','Pending'), ('Accepted','Accepted'),('Rejected','Rejected')])
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.request_from} -> {self.request_to} ({self.status})"