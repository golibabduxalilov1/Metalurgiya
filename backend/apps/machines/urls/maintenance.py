from django.urls import path
from apps.machines.views import MaintenanceAlertsView

urlpatterns = [
    path('alerts/', MaintenanceAlertsView.as_view(), name='maintenance-alerts'),
]
