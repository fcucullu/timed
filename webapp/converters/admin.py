from django.contrib import admin
from .models import ConversionHistory


class ConversionHistoryAdmin(admin.ModelAdmin):
    list_display = ('date', 'user', 'conversion_used', 'status')
    search_fields = ('user__username', 'conversion_used', 'status')

    class Meta:
        verbose_name = "Conversion history"
        verbose_name_plural = "Conversion histories"


admin.site.register(ConversionHistory, ConversionHistoryAdmin)
