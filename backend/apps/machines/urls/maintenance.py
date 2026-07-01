from django.urls import path
from apps.machines.views import MaintenanceAlertsView, MaintenanceExportView

urlpatterns = [
    path('alerts/', MaintenanceAlertsView.as_view(), name='maintenance-alerts'),
    path('export/', MaintenanceExportView.as_view(), name='maintenance-export'),
]
