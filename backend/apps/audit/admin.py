from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user', 'action', 'object_type', 'object_repr', 'ip_address')
    list_filter = ('action', 'object_type')
    search_fields = ('user__last_name', 'user__first_name', 'object_repr', 'ip_address')
