from django.contrib import admin
from .models import Workshop, Section


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'workshop', 'is_active')
    list_filter = ('workshop', 'is_active')
    search_fields = ('name', 'code', 'workshop__name')
