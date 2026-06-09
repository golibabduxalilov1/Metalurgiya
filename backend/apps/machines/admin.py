from django.contrib import admin
from .models import MachineType, MachineStatus, Machine, MachineStatusHistory, MachineAttachment, MachineAssignment


@admin.register(MachineType)
class MachineTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(MachineStatus)
class MachineStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'sort_order', 'requires_comment', 'is_active')
    list_filter = ('color', 'is_active')
    search_fields = ('name',)


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('inventory_number', 'name', 'model', 'machine_type', 'current_status', 'workshop', 'assigned_operator')
    list_filter = ('machine_type', 'current_status', 'workshop')
    search_fields = ('inventory_number', 'name', 'model', 'manufacturer')


@admin.register(MachineStatusHistory)
class MachineStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('machine', 'previous_status', 'new_status', 'changed_by', 'changed_at')
    list_filter = ('new_status',)
    search_fields = ('machine__inventory_number', 'machine__name', 'comment')


@admin.register(MachineAttachment)
class MachineAttachmentAdmin(admin.ModelAdmin):
    list_display = ('machine', 'original_filename', 'content_type', 'uploaded_by', 'uploaded_at')
    list_filter = ('content_type',)
    search_fields = ('machine__inventory_number', 'original_filename', 'description')


@admin.register(MachineAssignment)
class MachineAssignmentAdmin(admin.ModelAdmin):
    list_display = ('machine', 'operator', 'is_current', 'assigned_by', 'assigned_at')
    list_filter = ('is_current',)
    search_fields = ('machine__inventory_number', 'operator__last_name', 'operator__first_name')
