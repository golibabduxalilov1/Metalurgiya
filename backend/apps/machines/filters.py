"""
Machines App Filters
"""
import django_filters
from .models import Machine


class MachineFilter(django_filters.FilterSet):
    status = django_filters.NumberFilter(field_name='current_status__id')
    workshop = django_filters.NumberFilter(field_name='workshop__id')
    section = django_filters.NumberFilter(field_name='section__id')
    machine_type = django_filters.NumberFilter(field_name='machine_type__id')
    operator = django_filters.NumberFilter(field_name='assigned_operator__id')
    year_from = django_filters.NumberFilter(field_name='year_manufactured', lookup_expr='gte')
    year_to = django_filters.NumberFilter(field_name='year_manufactured', lookup_expr='lte')
    commissioned_from = django_filters.DateFilter(field_name='commissioned_date', lookup_expr='gte')
    commissioned_to = django_filters.DateFilter(field_name='commissioned_date', lookup_expr='lte')

    class Meta:
        model = Machine
        fields = ['status', 'workshop', 'section', 'machine_type', 'operator']
