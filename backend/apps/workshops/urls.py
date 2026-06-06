from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkshopViewSet, SectionViewSet

router = DefaultRouter()
router.register('sections', SectionViewSet, basename='sections')
router.register('', WorkshopViewSet, basename='workshops')

urlpatterns = [path('', include(router.urls))]
