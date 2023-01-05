from django.conf import settings as django_settings
from rrap.organizations.models import Organization, OrganisationPage
from rrap.datasets.models import Dataset
from rrap.core.models import Location, Topic
from rrap.invites.constants import InviteStatus


def settings(request):
    if request.user.is_authenticated:
        pending_invitations = request.user.invites_received.filter(
            status=InviteStatus.PENDING
        )
        total_pending_invitations = pending_invitations.count()

    else:
        pending_invitations = None
        total_pending_invitations = 0
    return {
        "rrap_logo": "http://127.0.0.1:8000/static/images/logo/logo.png",
        "rrap_version": django_settings.RRAP_VERSION,
        "rrap_environment": django_settings.RRAP_ENVIRONMENT,
        "recaptcha_enabled": django_settings.GOOGLE_RECAPTCHA_ENABLED,
        "recaptcha_site_key": django_settings.GOOGLE_RECAPTCHA_SITE_KEY,
        "google_analytics_ua": django_settings.GOOGLE_ANALYTICS_UA,
        "sentry_dsn": django_settings.SENTRY_DSN,
        "total_topics": Topic.objects.count(),
        "total_datasets": Dataset.objects.count(),
        "total_organisations": OrganisationPage.objects.count(),
        "total_locations": Location.objects.count(),
        "pending_invitations": pending_invitations,
        "total_pending_invitations": total_pending_invitations,
    }
