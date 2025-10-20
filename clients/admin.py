from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'company', 'created_by', 'created_at')
    search_fields = ('name', 'email', 'phone', 'company')
    list_filter = ('created_at', 'created_by')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Información Adicional', {
            'fields': ('company', 'address')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )
