from django.contrib import admin
from .models import UserToken

class UserTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at', 'used')

admin.site.register(UserToken, UserTokenAdmin)