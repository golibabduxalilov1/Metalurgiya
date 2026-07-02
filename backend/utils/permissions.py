"""
Utils - Permissions, Pagination, Middleware, Validators, Exceptions
"""
import logging
import re
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import permissions, pagination, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger('django')


# ============================================================
# Permissions
# ============================================================

class IsAdmin(permissions.BasePermission):
    """Only administrators"""
    message = 'Доступ разрешен только администраторам'

    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated
                and request.user.role == 'admin')


class IsAdminOrMaster(permissions.BasePermission):
    """Administrators and masters"""
    message = 'Доступ разрешен администраторам и мастерам'

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return request.user.role in ('admin', 'master')


class IsAdminOrMasterOrOwner(permissions.BasePermission):
    """All authenticated users can read; write is restricted"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


def section_access(section_key):
    """Permission class factory: allows admins OR users with the section in allowed_sections."""
    class SectionAccess(permissions.BasePermission):
        def has_permission(self, request, view):
            if not (request.user and request.user.is_authenticated):
                return False
            if request.user.role == 'admin':
                return True
            allowed = getattr(request.user, 'allowed_sections', None)
            return bool(allowed and section_key in allowed)
    SectionAccess.__name__ = f'SectionAccess_{section_key}'
    return SectionAccess


# ============================================================
# Pagination
# ============================================================

class StandardPagination(pagination.PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'page_size': self.get_page_size(self.request),
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                'count': {'type': 'integer'},
                'total_pages': {'type': 'integer'},
                'current_page': {'type': 'integer'},
                'page_size': {'type': 'integer'},
                'next': {'type': 'string', 'nullable': True},
                'previous': {'type': 'string', 'nullable': True},
                'results': schema,
            }
        }


# ============================================================
# Middleware
# ============================================================

class AuditMiddleware:
    """Store request in thread-local for audit logging"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from apps.audit.signals import _request_local
        _request_local.request = request
        response = self.get_response(request)
        if hasattr(_request_local, 'request'):
            del _request_local.request
        return response


# ============================================================
# Validators
# ============================================================

class AlphanumericPasswordValidator:
    """Password must contain at least one letter and one digit"""
    def validate(self, password, user=None):
        if not re.search(r'[A-Za-zА-Яа-я]', password):
            raise DjangoValidationError('Пароль должен содержать хотя бы одну букву')
        if not re.search(r'\d', password):
            raise DjangoValidationError('Пароль должен содержать хотя бы одну цифру')

    def get_help_text(self):
        return 'Пароль должен содержать буквы и цифры'


# ============================================================
# Exception Handler
# ============================================================

def custom_exception_handler(exc, context):
    if isinstance(exc, DjangoValidationError):
        exc = ValidationError(detail=exc.messages)

    response = exception_handler(exc, context)

    request = context.get('request')
    view = context.get('view')
    user = getattr(request, 'user', None)
    log_extra = (
        f"path={getattr(request, 'path', '?')} "
        f"method={getattr(request, 'method', '?')} "
        f"view={view.__class__.__name__ if view else '?'} "
        f"user={user if user and getattr(user, 'is_authenticated', False) else 'anonymous'}"
    )

    if response is None or response.status_code >= 500:
        logger.error('API exception: %s | %s', exc, log_extra, exc_info=exc)

    if response is not None:
        error_data = {
            'status': 'error',
            'code': response.status_code,
        }

        if isinstance(response.data, dict):
            if 'detail' in response.data:
                error_data['message'] = response.data['detail']
                if len(response.data) > 1:
                    error_data['errors'] = {k: v for k, v in response.data.items() if k != 'detail'}
            else:
                error_data['message'] = 'Ошибка валидации'
                error_data['errors'] = response.data
        elif isinstance(response.data, list):
            error_data['message'] = response.data[0] if response.data else 'Ошибка'
        else:
            error_data['message'] = str(response.data)

        response.data = error_data

    return response
