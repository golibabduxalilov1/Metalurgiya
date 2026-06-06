"""
Audit App - Журнал действий пользователей
"""
from django.db import models
from django.conf import settings
from rest_framework import serializers, generics
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django_filters import rest_framework as filters

from utils.permissions import IsAdmin


class AuditLog(models.Model):
    """Журнал всех действий в системе"""
    class ActionType(models.TextChoices):
        CREATE = 'create', 'Создание'
        UPDATE = 'update', 'Изменение'
        DELETE = 'delete', 'Удаление'
        RESTORE = 'restore', 'Восстановление'
        STATUS_CHANGE = 'status_change', 'Смена статуса'
        LOGIN = 'login', 'Вход'
        LOGOUT = 'logout', 'Выход'
        IMPORT = 'import', 'Импорт'
        EXPORT = 'export', 'Экспорт'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name='audit_logs', verbose_name='Пользователь',
        null=True, blank=True
    )
    action = models.CharField('Действие', max_length=30, choices=ActionType.choices)
    object_type = models.CharField('Тип объекта', max_length=100)
    object_id = models.PositiveBigIntegerField('ID объекта', null=True, blank=True)
    object_repr = models.CharField('Объект', max_length=500, blank=True)
    old_value = models.JSONField('Старое значение', null=True, blank=True)
    new_value = models.JSONField('Новое значение', null=True, blank=True)
    ip_address = models.GenericIPAddressField('IP адрес', null=True, blank=True)
    user_agent = models.CharField('User Agent', max_length=500, blank=True)
    created_at = models.DateTimeField('Время', auto_now_add=True)

    class Meta:
        db_table = 'audit_logs'
        verbose_name = 'Запись журнала'
        verbose_name_plural = 'Журнал действий'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['object_type', 'object_id']),
            models.Index(fields=['action', 'created_at']),
        ]

    def __str__(self):
        return f"{self.user} → {self.action} {self.object_type} ({self.created_at:%d.%m.%Y %H:%M})"


class AuditLogSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    action_display = serializers.CharField(source='get_action_display', read_only=True)

    class Meta:
        model = AuditLog
        fields = ['id', 'user', 'user_name', 'action', 'action_display',
                  'object_type', 'object_id', 'object_repr',
                  'old_value', 'new_value', 'ip_address', 'created_at']

    def get_user_name(self, obj):
        return obj.user.get_full_name() if obj.user else 'Система'


class AuditLogFilter(filters.FilterSet):
    user = filters.NumberFilter(field_name='user__id')
    action = filters.ChoiceFilter(choices=AuditLog.ActionType.choices)
    object_type = filters.CharFilter(lookup_expr='icontains')
    date_from = filters.DateFilter(field_name='created_at', lookup_expr='date__gte')
    date_to = filters.DateFilter(field_name='created_at', lookup_expr='date__lte')

    class Meta:
        model = AuditLog
        fields = ['user', 'action', 'object_type', 'date_from', 'date_to']


@extend_schema(tags=['audit'])
class AuditLogListView(generics.ListAPIView):
    """Журнал действий (только для администраторов)"""
    queryset = AuditLog.objects.select_related('user').all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdmin]
    filterset_class = AuditLogFilter
    search_fields = ['object_repr', 'user__last_name', 'user__first_name']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
