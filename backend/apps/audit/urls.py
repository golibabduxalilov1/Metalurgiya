from django.urls import path
from .models import AuditLogListView

urlpatterns = [
    path('', AuditLogListView.as_view(), name='audit-list'),
]
