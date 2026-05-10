from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.role != role:
                messages.error(request, 'You do not have permission to access that page.')
                return redirect('feed')
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


creator_required = role_required('creator')
consumer_required = role_required('consumer')
