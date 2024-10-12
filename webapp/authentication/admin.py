from django.contrib import admin
from .models import AuthenticationToken, CustomUser

class UserTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at', 'used')

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'company', 'email', 'is_active', 'is_staff', 'date_joined', 'api_key')
    verbose_name = "User"
    verbose_name_plural = "Users"

admin.site.register(AuthenticationToken, UserTokenAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
