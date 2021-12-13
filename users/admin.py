from django.contrib import admin
from .models import Profile

class UsersProfile(admin.ModelAdmin):
    list_display = ('user','company')
    list_filter = ('company',)

admin.site.register(Profile,UsersProfile)
