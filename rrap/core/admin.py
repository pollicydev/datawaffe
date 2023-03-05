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


class DataUsersButtonHelper(ButtonHelper):
    # Define classes for our button, here we can set an icon for example
    approve_button_classnames = ["icon", "icon-tick"]
    reject_button_classnames = ["no", "icon", "icon-cross"]

    def approve_button(self, obj):
        approve_text = "Approve"
        approve_text_inspect = "Approve {}".format(obj.name)
        index_view = not isinstance(self.view, InspectView)
        return {
            # "url": self.url_helper.create_url,
            "label": approve_text if index_view else approve_text_inspect,
            "classname": self.finalise_classname(
                ["button-small" if index_view else "button"]
                + self.approve_button_classnames
            ),
            "title": approve_text if index_view else approve_text_inspect,
        }

    def reject_button(self, obj):
        text = "Reject"
        small = not isinstance(self.view, InspectView)
        return {
            "url": self.url_helper.get_action_url("edit", quote(obj.pk)),
            "label": text,
            "classname": self.finalise_classname(
                ["button-small" if small else "button"] + self.reject_button_classnames
            ),
            "title": text,
        }

    def get_buttons_for_obj(
        self, obj, exclude=None, classnames_add=None, classnames_exclude=None
    ):
        """
        This function is used to gather all available buttons.
        We append our custom button to the btns list.
        """
        btns = super().get_buttons_for_obj(
            obj, exclude, classnames_add, classnames_exclude
        )
        if "view" not in (exclude or []):
            btns.append(self.approve_button(obj))
            btns.append(self.reject_button(obj))
        return btns


class DataUsersAdmin(ModelAdmin):
    model = Profile
    permission_helper_class = DataUsersValidationHelper
    menu_label = "Data Users"
    menu_icon = "group"
    menu_order = 100
    list_display = (
        # "profile_avatar",
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
    # inspect_template_name = "wagtailadmin/profile_inspect.html"
    list_export = (
        "profile_name",
        "profile_email",
        "country",
        "why",
        "review_status",
        "date_joined",
    )
    export_filename = "dw_data_users_list"
    button_helper_class = DataUsersButtonHelper

    def profile_name(self, obj):
        return obj.name

    def profile_email(self, obj):
        return obj.user.email

    def profile_avatar(self, obj):
        from django.utils.html import escape

        # styling not possible. Want width&height at 100px and 50% border radius
        return '<img style="width:100px" class="rounded" src="%s" />' % escape(
            obj.avatar.url
        )

    def get_extra_attrs_for_field_col(self, obj, field_name):
        if field_name == "review_status":
            return {"style": f"color: {obj.state_color()};text-transform: uppercase;"}
        return {}

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Only show people that aren't staff (moderator/editor)
        return qs.exclude(user__is_staff=True)

    profile_name.short_description = "Name or Alias"
    profile_email.short_description = "Email address"
    profile_avatar.short_description = "Avatar"
    profile_avatar.allow_tags = True


modeladmin_register(DataUsersAdmin)
modeladmin_register(BlogAdmin)
modeladmin_register(OrganisationsGroup)
modeladmin_register(PublicationsAdmin)
modeladmin_register(LocationsAdmin)
