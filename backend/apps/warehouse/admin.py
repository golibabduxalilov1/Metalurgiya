from django.contrib import admin
from .models import SparePart, UnitOfMeasure


@admin.register(UnitOfMeasure)
class UnitOfMeasureAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name']
    search_fields = ['name', 'short_name']


@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'unit', 'price', 'supplier', 'created_at']
    search_fields = ['name', 'supplier']
    filter_horizontal = ['machines']
