from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from utils.permissions import IsAdminOrMaster
from .models import SparePart
from .serializers import SparePartSerializer


class SparePartViewSet(viewsets.ModelViewSet):
    """Управление запчастями склада"""
    queryset = SparePart.objects.prefetch_related('machines').select_related('created_by').all()
    serializer_class = SparePartSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'supplier']
    ordering_fields = ['name', 'price', 'created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        return [IsAdminOrMaster()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
