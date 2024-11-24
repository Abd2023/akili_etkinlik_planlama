# user_management/decorators.py

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def admin_required(function=None, redirect_field_name=None, login_url='login'):
    """
    Decorator for views that checks that the user is an admin (is_superuser).
    Redirects to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
