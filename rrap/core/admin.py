from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)
from rrap.core.models import (
    Location,
    Topic,
    KeyPopulation,
    Service,
    Issue,
    Violation,
    PublicationType,
    PublicationPage,
)
from rrap.blog.models import BlogPageType, BlogPage
from rrap.organizations.models import OrganisationPage
from wagtail.contrib.modeladmin.helpers import PermissionHelper
from wagtail.contrib.modeladmin.mixins import ThumbnailMixin


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


class OrganisationsAdmin(ThumbnailMixin, ModelAdmin):
    """Organisations admin."""

    model = OrganisationPage
    menu_label = "Organisations"
    menu_icon = "group"
    menu_order = 100
    add_to_settings_menu = False
    exclude_from_explorer = False
    thumb_image_field_name = "logo"
    list_display = (
        "admin_thumb",
        "title",
    )

    thumb_image_filter_spec = "fill-300x150"
    thumb_image_width = 100
    thumb_col_header_text = "Logo"
    list_filter = ("status", "communities", "services", "issues")
    search_fields = ("title",)


class PublicationsAdmin(ThumbnailMixin, ModelAdmin):
    """Publications admin."""

    model = PublicationPage
    menu_label = "Publications"
    menu_icon = "group"
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
    menu_label = "Locations"
    menu_icon = "snippet"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name",)
    search_fields = ("name",)
    permission_helper_class = LocationsValidationPermissionHelper
    inspect_view_enabled = True


class TopicsAdmin(ModelAdmin):
    """Topics admin."""

    model = Topic
    menu_label = "Topics"
    menu_icon = "snippet"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name",)
    search_fields = ("name",)


class KeyPopAdmin(ModelAdmin):
    """Key populations admin."""

    model = KeyPopulation
    menu_label = "Key Populations"
    menu_icon = "snippet"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("title",)
    search_fields = ("title",)
    permission_helper_class = GenericValidationPermissionHelper
    inspect_view_enabled = True


class ServicesAdmin(ModelAdmin):
    """Services admin."""

    model = Service
    menu_label = "Services"
    menu_icon = "snippet"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("title",)
    search_fields = ("title",)
    permission_helper_class = GenericValidationPermissionHelper
    inspect_view_enabled = True


class IssuesAdmin(ModelAdmin):
    """Issues admin."""

    model = Issue
    menu_label = "Issues"
    menu_icon = "snippet"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("title",)
    search_fields = ("title",)
    permission_helper_class = GenericValidationPermissionHelper
    inspect_view_enabled = True


class ViolationsAdmin(ModelAdmin):
    """Violations admin."""

    model = Violation
    menu_label = "Violations"
    menu_icon = "snippet"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("title",)
    search_fields = ("title",)
    permission_helper_class = GenericValidationPermissionHelper
    inspect_view_enabled = True


class PubTypesAdmin(ModelAdmin):
    """Publication types admin."""

    model = PublicationType
    menu_label = "Publication Types"
    menu_icon = "snippet"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name",)
    search_fields = ("name",)
    # permission_helper_class = GenericValidationPermissionHelper


class BlogTypesAdmin(ModelAdmin):
    """Blog post types admin."""

    model = BlogPageType
    menu_label = "Blog Post Types"
    menu_icon = "snippet"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name",)
    search_fields = ("name",)
    # permission_helper_class = GenericValidationPermissionHelper


class MetaSettingsGroup(ModelAdminGroup):
    menu_label = "Metadata"
    menu_icon = "cog"
    menu_order = 300
    items = (
        LocationsAdmin,
        TopicsAdmin,
        KeyPopAdmin,
        ServicesAdmin,
        IssuesAdmin,
        ViolationsAdmin,
        BlogTypesAdmin,
        PubTypesAdmin,
    )


modeladmin_register(BlogAdmin)
modeladmin_register(OrganisationsAdmin)
modeladmin_register(PublicationsAdmin)
modeladmin_register(MetaSettingsGroup)
