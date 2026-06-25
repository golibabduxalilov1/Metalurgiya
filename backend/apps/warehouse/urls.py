from rest_framework.routers import DefaultRouter
from .views import SparePartViewSet, UnitOfMeasureViewSet

router = DefaultRouter()
router.register('units', UnitOfMeasureViewSet, basename='units')
router.register('', SparePartViewSet, basename='spare-parts')

urlpatterns = router.urls
