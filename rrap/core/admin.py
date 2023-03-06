from django.contrib.admin.utils import quote
from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)
from rrap.core.models import (
    Location,
    PublicationPage,
)
from rrap.blog.models import BlogPage
from rrap.organizations.models import (
    SexWorkOrganisation,
    LGBTQOrganisation,
    PWUIDSOrganisation,
)
from wagtail.contrib.modeladmin.mixins import ThumbnailMixin
from wagtail.contrib.modeladmin.views import InspectView
from wagtail.contrib.modeladmin.helpers import (
    PermissionHelper,
    ButtonHelper,
    AdminURLHelper,
)
from rrap.users.models import Profile


class LocationsValidationPermissionHelper(PermissionHelper):
    def user_can_list(self, user):
        return True

    def user_can_create(self, user):
        return False

    def user_can_edit_obj(self, user, obj):
        return False

    def user_can_delete_obj(self, user, obj):
        return False


class GenericValidationPermissionHelper(PermissionHelper):
    def user_can_list(self, user):
        return True

    def user_can_create(self, user):
        return False

    def user_can_edit_obj(self, user, obj):
        return True

    def user_can_delete_obj(self, user, obj):
        return False


class BlogAdmin(ThumbnailMixin, ModelAdmin):
    """Blogs admin."""

    model = BlogPage
    menu_label = "Blog Posts"
    menu_icon = "list-ul"
    menu_order = 100
    add_to_settings_menu = False
    exclude_from_explorer = False
    thumb_image_field_name = "image"
    list_display = (
        "admin_thumb",
        "title",
        "date",
    )

    thumb_image_filter_spec = "fill-300x150"
    thumb_image_width = 100
    thumb_col_header_text = "Featured image"
    list_filter = (
        "blog_page_type",
        "topics",
        "organisations",
    )
    search_fields = ("title", "introduction")


class LGBTQOrganisationsAdmin(ThumbnailMixin, ModelAdmin):

    model = LGBTQOrganisation
    menu_label = "LGBTQ"
    menu_icon = "group"
    menu_order = 100
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = (
        "title",
        "pwd_support",
        "status",
    )
    ordering = ("first_published_at",)
    list_filter = ("status", "communities", "services")
    search_fields = ("title",)

    def pwd_support(self, obj):
        return obj.support_pwds

    pwd_support.short_description = "Supports PWDs?"


class SWOrganisationsAdmin(ThumbnailMixin, ModelAdmin):

    model = SexWorkOrganisation
    menu_label = "Sex Workers"
    menu_icon = "group"
    menu_order = 100
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = (
        "title",
        "pwd_support",
        "status",
    )
    ordering = ("first_published_at",)
    list_filter = ("status", "communities", "services")
    search_fields = ("title",)

    def pwd_support(self, obj):
        return obj.support_pwds

    pwd_support.short_description = "Supports PWDs?"


class PWUIDsOrganisationsAdmin(ThumbnailMixin, ModelAdmin):

    model = PWUIDSOrganisation
    menu_label = "PWUIDs"
    menu_icon = "group"
    menu_order = 100
    add_to_settings_menu = False
    exclude_from_explorer = False
    thumb_image_field_name = "logo"
    list_display = (
        "title",
        "pwd_support",
        "status",
    )
    ordering = ("first_published_at",)
    list_filter = ("status", "communities", "services")
    search_fields = ("title",)

    def pwd_support(self, obj):
        return obj.support_pwds

    pwd_support.short_description = "Supports PWDs?"


class PublicationsAdmin(ThumbnailMixin, ModelAdmin):
    """Publications admin."""

    model = PublicationPage
    menu_label = "Publications"
    menu_icon = "doc-empty-inverse"
    menu_order = 100
    add_to_settings_menu = False
    exclude_from_explorer = False
    thumb_image_field_name = "thumbnail"
    list_display = (
        "admin_thumb",
        "title",
        "privacy",
        "date_published",
    )

    thumb_image_filter_spec = "fill-80x100"
    thumb_image_width = 72
    thumb_col_header_text = "Thumbnail"
    list_filter = (
        "topics",
        "pub_types",
        "organisations",
    )
    search_fields = (
        "title",
        "summary",
    )


class LocationsAdmin(ModelAdmin):
    """Locations admin."""

    model = Location
    menu_label = "Districts"
    menu_icon = "snippet"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name",)
    search_fields = ("name",)
    permission_helper_class = LocationsValidationPermissionHelper
    inspect_view_enabled = True


class OrganisationsGroup(ModelAdminGroup):
    menu_label = "Organisations"
    menu_icon = "group"
    menu_order = 100
    items = (
        LGBTQOrganisationsAdmin,
        SWOrganisationsAdmin,
        PWUIDsOrganisationsAdmin,
    )


modeladmin_register(BlogAdmin)
modeladmin_register(OrganisationsGroup)
modeladmin_register(PublicationsAdmin)
modeladmin_register(LocationsAdmin)
