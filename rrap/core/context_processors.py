from django.conf import settings as django_settings
from rrap.organizations.models import Organization
from rrap.datasets.models import Dataset
from rrap.core.models import Location
from rrap.invites.constants import InviteStatus


def settings(request):
    return {
        "rrap_logo": "http://127.0.0.1:8000/static/images/logo/logo.png",
        "rrap_version": django_settings.RRAP_VERSION,
        "rrap_environment": django_settings.RRAP_ENVIRONMENT,
        "recaptcha_enabled": django_settings.GOOGLE_RECAPTCHA_ENABLED,
        "recaptcha_site_key": django_settings.GOOGLE_RECAPTCHA_SITE_KEY,
        "google_analytics_ua": django_settings.GOOGLE_ANALYTICS_UA,
        "sentry_dsn": django_settings.SENTRY_DSN,
        "total_datasets": Dataset.objects.count(),
        "total_organizations": Organization.objects.count(),
        "total_locations": Location.objects.count(),
        "pending_invitations": request.user.invites_received.filter(
            status=InviteStatus.PENDING
        ),
        "total_pending_invitations": request.user.invites_received.filter(
            status=InviteStatus.PENDING
        ).count(),
    }
