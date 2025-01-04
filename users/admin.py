from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin
from django.contrib.auth.models import User
TokenAdmin.raw_id_fields = ['user']

