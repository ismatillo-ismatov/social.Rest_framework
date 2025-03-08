from django.contrib import admin
# from rest_framework.authtoken.admin import TokenAdmin, Token
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
@admin.register(Token)
class CustomTokenAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']


admin.site.unregister(Token)
admin.site.register(Token,CustomTokenAdmin)
# TokenAdmin.raw_id_fields = ['user']

