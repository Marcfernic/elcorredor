from django.contrib import admin
from django.contrib.auth.models import User
from .models import Property, Verification
# Register your models here.

admin.site.register(Property)
admin.site.register(Verification)