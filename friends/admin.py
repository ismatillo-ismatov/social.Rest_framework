from django.contrib import admin
from .models import FriendsRequest

# admin.site.register(FriendsRequest)

@admin.register(FriendsRequest)
class FriendsAdmin(admin.ModelAdmin):
    list_display = ('id', 'request_from',"request_to","status","created_at",)
    search_fields = ( 'request_from__username',"request_to__username","status",)
    list_filter = ('status',)