"""
Employees App - Справочник сотрудников/операторов
"""
from django.db import models
from rest_framework import serializers, viewsets
from drf_spectacular.utils import extend_schema
from utils.permissions import IsAdmin, IsAdminOrMaster


class Employee(models.Model):
    """Сотрудник / Оператор"""
    last_name = models.CharField('Фамилия', max_length=100)
    first_name = models.CharField('Имя', max_length=100)
    patronymic = models.CharField('Отчество', max_length=100, blank=True)
    position = models.CharField('Должность', max_length=200, blank=True)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    email = models.EmailField('Email', blank=True)
    workshop = models.ForeignKey(
        'workshops.Workshop', on_delete=models.SET_NULL,
        related_name='employees', verbose_name='Цех',
        null=True, blank=True
    )
    is_active = models.BooleanField('Активен', default=True)
    notes = models.TextField('Примечания', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'employees'
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        parts = [self.last_name, self.first_name]
        if self.patronymic:
            parts.append(self.patronymic)
        return ' '.join(parts)


class EmployeeSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    workshop_name = serializers.CharField(source='workshop.name', read_only=True)
    assigned_machines_count = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'last_name', 'first_name', 'patronymic', 'full_name',
                  'position', 'phone', 'email', 'workshop', 'workshop_name',
                  'is_active', 'notes', 'assigned_machines_count', 'created_at', 'updated_at']

    def get_full_name(self, obj):
        return obj.full_name

    def get_assigned_machines_count(self, obj):
        return obj.assigned_machines.filter(deleted_at__isnull=True).count()


@extend_schema(tags=['employees'])
class EmployeeViewSet(viewsets.ModelViewSet):
    """Справочник сотрудников и операторов"""
    queryset = Employee.objects.select_related('workshop').all()
    serializer_class = EmployeeSerializer
    search_fields = ['last_name', 'first_name', 'patronymic', 'position', 'phone']
    filterset_fields = ['workshop', 'is_active']
    ordering_fields = ['last_name', 'first_name', 'created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAdminOrMaster()]
        return [IsAdmin()]
