from rest_framework import serializers
from apps.machines.models import Machine
from .models import SparePart, UnitOfMeasure


class UnitOfMeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitOfMeasure
        fields = ['id', 'name', 'short_name']


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
    unit = serializers.PrimaryKeyRelatedField(
        queryset=UnitOfMeasure.objects.all(),
        allow_null=True,
        required=False
    )
    unit_data = UnitOfMeasureSerializer(source='unit', read_only=True)
    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model = SparePart
        fields = [
            'id', 'name', 'quantity', 'unit', 'unit_data', 'price', 'unit_price', 'supplier',
            'machines', 'machines_data',
            'created_by', 'created_by_name',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at', 'unit_price']

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None

    def validate(self, attrs):
        # unit_price is calculated ONLY on CREATE (first purchase).
        # On UPDATE it never changes — stock deductions must not affect unit price.
        if not self.instance:
            price = attrs.get('price')
            quantity = attrs.get('quantity')
            if price is not None and quantity and quantity != 0:
                from decimal import Decimal
                attrs['unit_price'] = Decimal(str(price)) / Decimal(str(quantity))
        return attrs
