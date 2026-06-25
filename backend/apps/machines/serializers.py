"""
Machines App Serializers
"""
from django.utils import timezone
from rest_framework import serializers

from apps.workshops.models import Workshop, Section
from apps.employees.models import Employee
from .models import Machine, MachineType, MachineStatus, MachineStatusHistory, MachineAttachment, MachineAssignment, MaintenanceSchedule, RepairTask, TaskSparePart, MaintenanceHistory


class MachineTypeSerializer(serializers.ModelSerializer):
    machines_count = serializers.SerializerMethodField()

    class Meta:
        model = MachineType
        fields = ['id', 'name', 'description', 'is_active', 'machines_count', 'created_at', 'updated_at']

    def get_machines_count(self, obj):
        return obj.machines.filter(deleted_at__isnull=True).count()


class MachineStatusSerializer(serializers.ModelSerializer):
    machines_count = serializers.SerializerMethodField()

    class Meta:
        model = MachineStatus
        fields = ['id', 'name', 'color', 'is_active', 'requires_comment',
                  'sort_order', 'machines_count', 'created_at', 'updated_at']

    def get_machines_count(self, obj):
        return obj.machines.filter(deleted_at__isnull=True).count()


class MachineStatusHistorySerializer(serializers.ModelSerializer):
    previous_status_name = serializers.CharField(source='previous_status.name', read_only=True)
    previous_status_color = serializers.CharField(source='previous_status.color', read_only=True)
    new_status_name = serializers.CharField(source='new_status.name', read_only=True)
    new_status_color = serializers.CharField(source='new_status.color', read_only=True)
    changed_by_name = serializers.SerializerMethodField()

    class Meta:
        model = MachineStatusHistory
        fields = ['id', 'machine', 'previous_status', 'previous_status_name', 'previous_status_color',
                  'new_status', 'new_status_name', 'new_status_color',
                  'changed_by', 'changed_by_name', 'comment', 'changed_at']
        read_only_fields = ['machine', 'previous_status', 'changed_by', 'changed_at']

    def get_changed_by_name(self, obj):
        return obj.changed_by.get_full_name() if obj.changed_by else None


class MachineAttachmentSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()
    file_size_display = serializers.SerializerMethodField()

    class Meta:
        model = MachineAttachment
        fields = ['id', 'machine', 'file', 'file_url', 'original_filename', 'file_size',
                  'file_size_display', 'content_type', 'description',
                  'uploaded_by', 'uploaded_by_name', 'uploaded_at']
        read_only_fields = ['machine', 'original_filename', 'file_size', 'content_type',
                            'uploaded_by', 'uploaded_at']

    def get_uploaded_by_name(self, obj):
        return obj.uploaded_by.get_full_name() if obj.uploaded_by else None

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None

    def get_file_size_display(self, obj):
        size = obj.file_size
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        else:
            return f"{size / (1024 * 1024):.1f} MB"


class MachineAttachmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineAttachment
        fields = ['file', 'description']

    def validate_file(self, value):
        max_size = 10 * 1024 * 1024  # 10MB
        if value.size > max_size:
            raise serializers.ValidationError('Размер файла не должен превышать 10 МБ')
        return value


class MachineAssignmentSerializer(serializers.ModelSerializer):
    operator_name = serializers.SerializerMethodField()
    assigned_by_name = serializers.SerializerMethodField()

    class Meta:
        model = MachineAssignment
        fields = ['id', 'machine', 'operator', 'operator_name', 'assigned_by',
                  'assigned_by_name', 'assigned_at', 'unassigned_at', 'is_current', 'notes']
        read_only_fields = ['machine', 'assigned_by', 'assigned_at', 'unassigned_at']

    def get_operator_name(self, obj):
        return obj.operator.full_name

    def get_assigned_by_name(self, obj):
        return obj.assigned_by.get_full_name() if obj.assigned_by else None


class MachineListSerializer(serializers.ModelSerializer):
    machine_type_name = serializers.CharField(source='machine_type.name', read_only=True)
    current_status_name = serializers.CharField(source='current_status.name', read_only=True)
    current_status_color = serializers.CharField(source='current_status.color', read_only=True)
    workshop_name = serializers.CharField(source='workshop.name', read_only=True)
    section_name = serializers.CharField(source='section.name', read_only=True)
    operator_name = serializers.SerializerMethodField()
    book_value = serializers.SerializerMethodField()

    class Meta:
        model = Machine
        fields = [
            'id', 'name', 'inventory_number', 'model', 'manufacturer',
            'machine_type', 'machine_type_name',
            'current_status', 'current_status_name', 'current_status_color',
            'workshop', 'workshop_name', 'section', 'section_name', 'workplace',
            'assigned_operator', 'operator_name', 'assigned_brigade',
            'initial_cost', 'useful_life_years', 'residual_value', 'book_value',
            'deleted_at', 'created_at', 'updated_at'
        ]

    def get_operator_name(self, obj):
        return obj.assigned_operator.full_name if obj.assigned_operator else None

    def get_book_value(self, obj):
        info = obj.amortization_info
        return info['book_value'] if info else None


class MachineDetailSerializer(serializers.ModelSerializer):
    machine_type_name = serializers.CharField(source='machine_type.name', read_only=True)
    current_status_data = MachineStatusSerializer(source='current_status', read_only=True)
    workshop_name = serializers.CharField(source='workshop.name', read_only=True)
    section_name = serializers.CharField(source='section.name', read_only=True)
    operator_data = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    attachments = MachineAttachmentSerializer(many=True, read_only=True)
    recent_status_history = serializers.SerializerMethodField()
    current_assignment = serializers.SerializerMethodField()

    amortization_info = serializers.SerializerMethodField()

    class Meta:
        model = Machine
        fields = [
            'id', 'name', 'inventory_number', 'model', 'manufacturer',
            'year_manufactured', 'commissioned_date',
            'machine_type', 'machine_type_name',
            'current_status', 'current_status_data',
            'workshop', 'workshop_name', 'section', 'section_name', 'workplace',
            'assigned_operator', 'operator_data', 'assigned_brigade',
            'initial_cost', 'useful_life_years', 'residual_value', 'amortization_info',
            'description', 'attachments', 'recent_status_history', 'current_assignment',
            'deleted_at', 'created_at', 'updated_at', 'created_by', 'created_by_name'
        ]

    def get_operator_data(self, obj):
        if obj.assigned_operator:
            return {
                'id': obj.assigned_operator.id,
                'full_name': obj.assigned_operator.full_name,
                'position': obj.assigned_operator.position,
            }
        return None

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None

    def get_recent_status_history(self, obj):
        history = obj.status_history.all()[:10]
        return MachineStatusHistorySerializer(history, many=True).data

    def get_current_assignment(self, obj):
        assignment = obj.assignments.filter(is_current=True).first()
        if assignment:
            return MachineAssignmentSerializer(assignment).data
        return None

    def get_amortization_info(self, obj):
        return obj.amortization_info


class MachineCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = [
            'id',
            'name', 'inventory_number', 'model', 'manufacturer',
            'year_manufactured', 'commissioned_date',
            'machine_type', 'current_status',
            'workshop', 'section', 'workplace',
            'assigned_operator', 'assigned_brigade', 'description',
            'initial_cost', 'useful_life_years', 'residual_value',
        ]
        read_only_fields = ['id']

    def validate_inventory_number(self, value):
        qs = Machine.objects.filter(inventory_number=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('Станок с таким инвентарным номером уже существует')
        return value


class TaskSparePartSerializer(serializers.ModelSerializer):
    spare_part_name = serializers.CharField(source='spare_part.name', read_only=True)
    unit_short = serializers.SerializerMethodField()

    class Meta:
        model = TaskSparePart
        fields = ['id', 'task', 'spare_part', 'spare_part_name', 'unit_short',
                  'quantity_used', 'notes', 'cost', 'deducted', 'created_at']
        read_only_fields = ['task', 'deducted', 'created_at']

    def get_unit_short(self, obj):
        if obj.spare_part.unit:
            return obj.spare_part.unit.short_name or obj.spare_part.unit.name
        return None


class RepairTaskSerializer(serializers.ModelSerializer):
    assignee_name = serializers.SerializerMethodField()
    spare_parts_used = TaskSparePartSerializer(many=True, read_only=True)
    is_mine = serializers.SerializerMethodField()

    class Meta:
        model = RepairTask
        fields = ['id', 'schedule', 'title', 'assignee', 'assignee_name', 'due_date',
                  'is_done', 'done_at', 'created_at', 'spare_parts_used', 'is_mine']
        read_only_fields = ['schedule', 'done_at', 'created_at']

    def get_assignee_name(self, obj):
        if not obj.assignee:
            return None
        return f"{obj.assignee.get_full_name()} — {obj.assignee.get_role_display()}"

    def get_is_mine(self, obj):
        request = self.context.get('request')
        if not request:
            return False
        if request.user.role == 'admin':
            return True
        return obj.assignee_id == request.user.id


class MaintenanceHistorySerializer(serializers.ModelSerializer):
    completed_by_name = serializers.SerializerMethodField()

    class Meta:
        model = MaintenanceHistory
        fields = ['id', 'machine', 'repair_started_at', 'completed_at', 'completed_by',
                  'completed_by_name', 'interval_months', 'notes', 'tasks_snapshot', 'total_cost']
        read_only_fields = ['__all__']

    def get_completed_by_name(self, obj):
        if obj.completed_by:
            return obj.completed_by.get_full_name() or obj.completed_by.username
        return None


class MaintenanceScheduleSerializer(serializers.ModelSerializer):
    machine_name = serializers.CharField(source='machine.name', read_only=True)
    machine_inventory = serializers.CharField(source='machine.inventory_number', read_only=True)
    machine_workshop = serializers.CharField(source='machine.workshop.name', read_only=True)
    days_until = serializers.SerializerMethodField()
    alert_level = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    updated_by_name = serializers.SerializerMethodField()

    class Meta:
        model = MaintenanceSchedule
        fields = [
            'id', 'machine', 'machine_name', 'machine_inventory', 'machine_workshop',
            'interval_months', 'last_maintenance_date', 'next_maintenance_date',
            'notes', 'days_until', 'alert_level', 'in_repair', 'repair_started_at',
            'tasks_total', 'tasks_done', 'total_expense',
            'created_by', 'created_by_name', 'updated_by', 'updated_by_name',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['machine', 'created_by', 'updated_by', 'created_at', 'updated_at']

    def get_days_until(self, obj):
        return obj.days_until

    def get_alert_level(self, obj):
        return obj.alert_level

    def get_in_repair(self, obj):
        return obj.in_repair

    def get_tasks_total(self, obj):
        return obj.tasks_total

    def get_tasks_done(self, obj):
        return obj.tasks_done

    def get_total_expense(self, obj):
        from django.db.models import Sum
        from apps.machines.models import MaintenanceHistory
        result = MaintenanceHistory.objects.filter(machine=obj.machine).aggregate(
            total=Sum('total_cost')
        )
        return str(result['total'] or 0)

    in_repair = serializers.SerializerMethodField()
    tasks_total = serializers.SerializerMethodField()
    tasks_done = serializers.SerializerMethodField()
    total_expense = serializers.SerializerMethodField()

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None

    def get_updated_by_name(self, obj):
        return obj.updated_by.get_full_name() if obj.updated_by else None


class MaintenanceScheduleWriteSerializer(serializers.ModelSerializer):
    next_maintenance_date = serializers.DateField(required=False, write_only=True)

    class Meta:
        model = MaintenanceSchedule
        fields = ['interval_months', 'last_maintenance_date', 'next_maintenance_date', 'notes']
        extra_kwargs = {
            'last_maintenance_date': {'required': False, 'allow_null': True},
        }

    def validate(self, attrs):
        from dateutil.relativedelta import relativedelta
        next_date = attrs.pop('next_maintenance_date', None)
        last_date = attrs.get('last_maintenance_date')
        interval = attrs.get('interval_months')
        if next_date and interval:
            # Direct next date provided — calculate last_maintenance_date backwards
            attrs['next_maintenance_date'] = next_date
            if not last_date:
                attrs['last_maintenance_date'] = next_date - relativedelta(months=interval)
        elif last_date and interval:
            attrs['next_maintenance_date'] = last_date + relativedelta(months=interval)
        else:
            from rest_framework.exceptions import ValidationError
            raise ValidationError('next_maintenance_date yoki last_maintenance_date talab qilinadi')
        return attrs


class MaintenanceCompleteSerializer(serializers.Serializer):
    completion_date = serializers.DateField()
    notes = serializers.CharField(required=False, allow_blank=True)

    def validate_completion_date(self, value):
        from django.utils import timezone
        if value > timezone.now().date():
            raise serializers.ValidationError('Дата завершения ТО не может быть в будущем')
        return value


class ChangeStatusSerializer(serializers.Serializer):
    status_id = serializers.IntegerField()
    comment = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        try:
            status = MachineStatus.objects.get(id=attrs['status_id'], is_active=True)
        except MachineStatus.DoesNotExist:
            raise serializers.ValidationError({'status_id': 'Статус не найден'})

        if status.requires_comment and not attrs.get('comment'):
            raise serializers.ValidationError({'comment': 'Комментарий обязателен для данного статуса'})

        attrs['status'] = status
        return attrs
