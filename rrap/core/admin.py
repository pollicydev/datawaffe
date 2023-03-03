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
from wagtail.contrib.modeladmin.helpers import PermissionHelper
from wagtail.contrib.modeladmin.mixins import ThumbnailMixin
from wagtail.contrib.modeladmin.helpers import PermissionHelper
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


class DataUsersValidationHelper(PermissionHelper):
    def user_can_list(self, user):
        return True

    def user_can_create(self, user):
        return False

    def user_can_edit_obj(self, user, obj):
        return False

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
    thumb_image_field_name = "logo"
    list_display = (
        "admin_thumb",
        "title",
    )
    ordering = ("first_published_at",)
    thumb_image_filter_spec = "fill-300x150"
    thumb_image_width = 100
    thumb_col_header_text = "Logo"
    list_filter = ("status", "communities", "services")
    search_fields = ("title",)


class SWOrganisationsAdmin(ThumbnailMixin, ModelAdmin):

    model = SexWorkOrganisation
    menu_label = "Sex Workers"
    menu_icon = "group"
    menu_order = 100
    add_to_settings_menu = False
    exclude_from_explorer = False
    thumb_image_field_name = "logo"
    list_display = (
        "admin_thumb",
        "title",
    )
    ordering = ("first_published_at",)
    thumb_image_filter_spec = "fill-300x150"
    thumb_image_width = 100
    thumb_col_header_text = "Logo"
    list_filter = ("status", "communities", "services")
    search_fields = ("title",)


class PWUIDsOrganisationsAdmin(ThumbnailMixin, ModelAdmin):

    model = PWUIDSOrganisation
    menu_label = "PWUIDs"
    menu_icon = "group"
    menu_order = 100
    add_to_settings_menu = False
    exclude_from_explorer = False
    thumb_image_field_name = "logo"
    list_display = (
        "admin_thumb",
        "title",
    )
    ordering = ("first_published_at",)
    thumb_image_filter_spec = "fill-300x150"
    thumb_image_width = 100
    thumb_col_header_text = "Logo"
    list_filter = ("status", "services")
    search_fields = ("title",)


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


class DataUsersAdmin(ModelAdmin):
    model = Profile
    permission_helper_class = DataUsersValidationHelper
    menu_label = "Data Users"
    menu_icon = "group"
    menu_order = 100
    list_display = (
        "profile_name",
        "profile_email",
        "country",
        "review_status",
        "date_joined",
    )
    ordering = ("name",)
    list_filter = ("review_status",)
    search_fields = ("name", "email")
    inspect_view_enabled = True
    list_export = (
        "profile_name",
        "profile_email",
        "country",
        "why",
        "review_status",
        "date_joined",
    )
    export_filename = "dw_data_users_list"

    def profile_name(self, obj):
        return obj.name

    def profile_email(self, obj):
        return obj.user.email

    profile_name.short_description = "Name or Alias"
    profile_email.short_description = "Email address"


modeladmin_register(DataUsersAdmin)
modeladmin_register(BlogAdmin)
modeladmin_register(OrganisationsGroup)
modeladmin_register(PublicationsAdmin)
modeladmin_register(LocationsAdmin)
