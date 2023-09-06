from functools import wraps
from django.http import HttpResponseForbidden

def require_executor(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not hasattr(request.user, 'executor_profile'):
            return HttpResponseForbidden("Вы не являетесь исполнителем")
        return view_func(request, *args, **kwargs)
    return _wrapped_view