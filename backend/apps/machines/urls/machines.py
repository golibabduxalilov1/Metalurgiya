from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.machines.views import MachineViewSet

router = DefaultRouter()
router.register('', MachineViewSet, basename='machines')

urlpatterns = [
    path('', include(router.urls)),
]
