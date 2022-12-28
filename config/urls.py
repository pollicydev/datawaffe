from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtailautocomplete.urls.admin import urlpatterns as autocomplete_admin_urls
from django.views.generic import TemplateView
from rrap.core import views as core_views

urlpatterns = [
    path("core/", include("rrap.core.urls", namespace="core")),
    # Wagtail URLs
    path("cms/autocomplete/", include(autocomplete_admin_urls)),
    path(settings.WAGTAIL_ADMIN_URL, include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("organizations/", include("rrap.organizations.urls")),
    path("data/", include("rrap.datasets.urls")),
    path("activity/", include("rrap.activities.urls", namespace="activities")),
    path("invitations/", include("rrap.invites.urls", namespace="invitations")),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    path("select2/", include("django_select2.urls")),
    # User management
    path("users/", include("rrap.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    path("map/", core_views.map, name="map"),
    path("publications/", core_views.publications_index, name="publications"),
    path("", include(wagtail_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
