from django.contrib import admin
from .models import Converter

class ConverterAdmin(admin.ModelAdmin):
    list_display = ('date', 'user', 'conversion_used', 'status')
    search_fields = ('user__username', 'conversion_used', 'status')
    list_per_page = 20

admin.site.register(Converter, ConverterAdmin)
