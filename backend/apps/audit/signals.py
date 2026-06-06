"""
Audit signals - functions for logging actions
"""
import threading

_request_local = threading.local()


def get_current_request():
    return getattr(_request_local, 'request', None)


def log_action(user, action, obj, old_value=None, new_value=None, request=None):
    """Log an action to the audit log"""
    from .models import AuditLog

    ip_address = None
    user_agent = ''

    if request:
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]

    def serialize_value(val):
        if val is None:
            return None
        if isinstance(val, dict):
            result = {}
            for k, v in val.items():
                try:
                    import json
                    json.dumps(v)
                    result[str(k)] = v
                except (TypeError, ValueError):
                    result[str(k)] = str(v)
            return result
        return str(val)

    try:
        AuditLog.objects.create(
            user=user,
            action=action,
            object_type=obj.__class__.__name__,
            object_id=getattr(obj, 'pk', None),
            object_repr=str(obj)[:500],
            old_value=serialize_value(old_value),
            new_value=serialize_value(new_value),
            ip_address=ip_address,
            user_agent=user_agent,
        )
    except Exception:
        pass  # Never break the main flow because of audit logging


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')
