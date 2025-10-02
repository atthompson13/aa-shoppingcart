from functools import wraps
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext as _

def permission_required_or_superuser(perm):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapped_view(request, *args, **kwargs):
            if request.user.is_superuser or request.user.has_perm(perm):
                return view_func(request, *args, **kwargs)
            messages.error(request, _('You do not have permission to access this page.'))
            return redirect('authentication:dashboard')
        return wrapped_view
    return decorator
