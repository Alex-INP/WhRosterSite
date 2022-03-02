from django.contrib import admin

from .models import NormalUser, UserProfile

# Register your models here.
admin.site.register(NormalUser)
admin.site.register(UserProfile)
