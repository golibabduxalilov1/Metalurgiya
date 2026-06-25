from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from utils.permissions import IsAdminOrMaster
from .models import SparePart, UnitOfMeasure
from .serializers import SparePartSerializer, UnitOfMeasureSerializer


class UnitOfMeasureViewSet(viewsets.ModelViewSet):
    queryset = UnitOfMeasure.objects.all()
    serializer_class = UnitOfMeasureSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'short_name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        return [IsAdminOrMaster()]


class SparePartViewSet(viewsets.ModelViewSet):
    """Управление запчастями склада"""
    queryset = (
        SparePart.objects
        .select_related('unit', 'created_by')
        .prefetch_related('machines')
        .all()
    )
    serializer_class = SparePartSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['machines']
    search_fields = ['name', 'supplier']
    ordering_fields = ['name', 'price', 'created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        return [IsAdminOrMaster()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
