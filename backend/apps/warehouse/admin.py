from django.contrib import admin
from .models import SparePart


@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'supplier', 'created_at']
    search_fields = ['name', 'supplier']
    filter_horizontal = ['machines']
