from django.conf import settings as django_settings


def settings(request):
    return {
        "rrap_version": django_settings.RRAP_VERSION,
        "rrap_environment": django_settings.RRAP_ENVIRONMENT,
        "recaptcha_enabled": django_settings.GOOGLE_RECAPTCHA_ENABLED,
        "recaptcha_site_key": django_settings.GOOGLE_RECAPTCHA_SITE_KEY,
        "google_analytics_ua": django_settings.GOOGLE_ANALYTICS_UA,
        "sentry_dsn": django_settings.SENTRY_DSN,
    }
