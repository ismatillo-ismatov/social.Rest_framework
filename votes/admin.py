from django.contrib import admin
from .models import Like
@admin.register(Like)
class Likes(admin.ModelAdmin):
    list_display = ('id','post','user','created_at')
