from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.machines.views import MachineTypeViewSet

router = DefaultRouter()
router.register('', MachineTypeViewSet, basename='machine-types')

urlpatterns = [path('', include(router.urls))]
