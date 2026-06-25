"""
URL Configuration for Machine Registry System
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

api_v1_urlpatterns = [
    path('auth/', include('apps.users.urls.auth')),
    path('users/', include('apps.users.urls.users')),
    path('machines/', include('apps.machines.urls.machines')),
    path('machine-types/', include('apps.machines.urls.machine_types')),
    path('statuses/', include('apps.machines.urls.statuses')),
    path('attachments/', include('apps.machines.urls.attachments')),
    path('workshops/', include('apps.workshops.urls')),
    path('employees/', include('apps.employees.urls')),
    path('audit/', include('apps.audit.urls')),
    path('maintenance/', include('apps.machines.urls.maintenance')),
    path('spare-parts/', include('apps.warehouse.urls')),
    path('dashboard/', __import__('apps.machines.dashboard', fromlist=['DashboardView']).DashboardView.as_view(), name='dashboard'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_v1_urlpatterns)),

    # Swagger / OpenAPI docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
