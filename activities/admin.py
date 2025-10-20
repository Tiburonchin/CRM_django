from django.contrib import admin
from .models import Activity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('client', 'type', 'status', 'date', 'created_by', 'created_at')
    search_fields = ('notes', 'client__name')
    list_filter = ('type', 'status', 'date', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Información Básica', {
            'fields': ('client', 'type', 'status', 'date')
        }),
        ('Detalles', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )
