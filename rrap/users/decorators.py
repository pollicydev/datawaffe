from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect


def onboarding_required(
    view_func=None,
    redirect_field_name=REDIRECT_FIELD_NAME,
    onboarding_url="users:onboarding",
):
    """
    Decorator for views that checks that the logged in user is fully onboarded,
    redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.profile.has_finished_registration,
        login_url=onboarding_url,
        redirect_field_name=redirect_field_name,
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator
