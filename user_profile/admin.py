from django.contrib import admin
from .models import UserProfile
# admin.site.register(UserProfile)

@admin.register(UserProfile)
class UserProfile(admin.ModelAdmin):
    list_display = ('id','userName')