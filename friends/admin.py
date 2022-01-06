from django.contrib import admin
from .models import FriendsRequest

# admin.site.register(FriendsRequest)

@admin.register(FriendsRequest)
class FriendsAdmin(admin.ModelAdmin):
    list_display = ['id', 'request_from',"request_to"]