from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.machines.views import MachineStatusViewSet

router = DefaultRouter()
router.register('', MachineStatusViewSet, basename='statuses')

urlpatterns = [path('', include(router.urls))]
