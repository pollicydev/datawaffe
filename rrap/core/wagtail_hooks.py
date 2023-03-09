from django.templatetags.static import static
from django.utils.html import format_html
from wagtail.core import hooks
from wagtail.admin.ui.components import Component
from django.contrib.auth import get_user_model
from rrap.organizations.models import (
    SexWorkOrganisation,
    LGBTQOrganisation,
    PWUIDSOrganisation,
)
from rrap.core.models import PublicationPage
from rrap.blog.models import BlogPage

User = get_user_model()


class DWSummaryPanel(Component):
    order = 50
    template_name = "wagtailadmin/dashboard_summary.html"

    def get_context_data(self, parent_context):
        context = super().get_context_data(parent_context)

        lgbtq_organisations = LGBTQOrganisation.objects.all().count()
        sw_organisations = SexWorkOrganisation.objects.all().count()
        pwuid_organisations = PWUIDSOrganisation.objects.all().count()
        publications = PublicationPage.objects.all().count()
        blogs = BlogPage.objects.all().count()
        users = User.objects.exclude(is_staff=True).exclude(is_superuser=True).count()

        context.update(
            {
                "lgbtq_organisations": lgbtq_organisations,
                "sw_organisations": sw_organisations,
                "pwuid_organisations": pwuid_organisations,
                "publications": publications,
                "blogs": blogs,
                "users": users,
            }
        )

        return context


@hooks.register("construct_homepage_panels")
def add_another_welcome_panel(request, panels):
    panels.append(DWSummaryPanel())


@hooks.register("insert_global_admin_css")
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">', static("css/custom-wagtail-admin.css")
    )
