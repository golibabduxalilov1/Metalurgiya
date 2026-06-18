from rest_framework.routers import DefaultRouter
from .views import SparePartViewSet

router = DefaultRouter()
router.register('', SparePartViewSet, basename='spare-parts')

urlpatterns = router.urls
