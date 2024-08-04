from django.contrib import admin
from authentication.models import User, Profile


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'email_verified']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
