from django.templatetags.static import static
from django.utils.html import format_html
from wagtail.core import hooks
from wagtail.admin.ui.components import Component
from django.utils.safestring import mark_safe
from rrap.organizations.models import OrganisationPage
from rrap.core.models import PublicationPage
from rrap.blog.models import BlogPage


class DWSummaryPanel(Component):
    order = 50
    template_name = "wagtailadmin/dashboard_summary.html"

    def get_context_data(self, parent_context):
        context = super().get_context_data(parent_context)

        organisations = OrganisationPage.objects.all().count()
        publications = PublicationPage.objects.all().count()
        blogs = BlogPage.objects.all().count()
        context.update(
            {
                "organisations": organisations,
                "publications": publications,
                "blogs": blogs,
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
