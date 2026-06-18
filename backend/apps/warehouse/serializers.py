from rest_framework import serializers
from apps.machines.models import Machine
from .models import SparePart


class MachineShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ['id', 'name', 'inventory_number']


class SparePartSerializer(serializers.ModelSerializer):
    machines_data = MachineShortSerializer(source='machines', many=True, read_only=True)
    machines = serializers.PrimaryKeyRelatedField(
        queryset=Machine.objects.filter(deleted_at__isnull=True),
        many=True,
        required=False
    )
    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model = SparePart
        fields = [
            'id', 'name', 'price', 'supplier',
            'machines', 'machines_data',
            'created_by', 'created_by_name',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None
