from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .models import EmployeeViewSet

router = DefaultRouter()
router.register('', EmployeeViewSet, basename='employees')

urlpatterns = [path('', include(router.urls))]
