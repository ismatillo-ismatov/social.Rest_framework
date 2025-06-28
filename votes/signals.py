from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Like
from notification.models import Notification
from posts.models import Post





