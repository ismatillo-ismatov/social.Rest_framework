from django.contrib import admin
from .models import Comment
# admin.site.register(Comment)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id",'owner','post','parent','comment','created_at',)
    search_fields = ('comment','owner__username','post__title')
    list_filter = ('created_at','post')