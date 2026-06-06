"""
Workshops App Serializers and Views
"""
from rest_framework import serializers, viewsets
from drf_spectacular.utils import extend_schema
from .models import Workshop, Section
from utils.permissions import IsAdmin, IsAdminOrMaster


class SectionSerializer(serializers.ModelSerializer):
    workshop_name = serializers.CharField(source='workshop.name', read_only=True)
    machines_count = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = ['id', 'workshop', 'workshop_name', 'name', 'code',
                  'description', 'is_active', 'machines_count', 'created_at', 'updated_at']

    def get_machines_count(self, obj):
        return obj.machines.filter(deleted_at__isnull=True).count()


class WorkshopSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)
    machines_count = serializers.SerializerMethodField()

    class Meta:
        model = Workshop
        fields = ['id', 'name', 'code', 'description', 'is_active',
                  'sections', 'machines_count', 'created_at', 'updated_at']

    def get_machines_count(self, obj):
        return obj.machines.filter(deleted_at__isnull=True).count()


@extend_schema(tags=['workshops'])
class WorkshopViewSet(viewsets.ModelViewSet):
    """Справочник цехов"""
    queryset = Workshop.objects.prefetch_related('sections').all()
    serializer_class = WorkshopSerializer
    search_fields = ['name', 'code']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        return [IsAdmin()]


@extend_schema(tags=['workshops'])
class SectionViewSet(viewsets.ModelViewSet):
    """Справочник участков"""
    queryset = Section.objects.select_related('workshop').all()
    serializer_class = SectionSerializer
    search_fields = ['name', 'code']
    filterset_fields = ['workshop']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        return [IsAdmin()]
