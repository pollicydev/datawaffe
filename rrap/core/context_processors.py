from django.conf import settings as django_settings
from rrap.organizations.models import OrganisationPage
from rrap.core.models import Location


def settings(request):

    return {
        "rrap_logo": "http://127.0.0.1:8000/static/images/logo/logo.png",
        "rrap_version": django_settings.RRAP_VERSION,
        "rrap_environment": django_settings.RRAP_ENVIRONMENT,
        "recaptcha_site_key": django_settings.RECAPTCHA_PUBLIC_KEY,
        "google_analytics_ua": django_settings.GOOGLE_ANALYTICS_UA,
        "mapbox_access_token": django_settings.MAPBOX_ACCESS_TOKEN,
        "sentry_dsn": django_settings.SENTRY_DSN,
        "total_organisations": OrganisationPage.objects.count(),
        "total_locations": Location.objects.count(),
    }
