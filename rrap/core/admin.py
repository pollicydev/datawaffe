from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)
from .models import (
    Location,
    Topic,
    KeyPopulation,
    Service,
    Issue,
    Violation,
    PublicationType,
)
from wagtail.contrib.modeladmin.helpers import PermissionHelper


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


class LocationsAdmin(ModelAdmin):
    """Locations admin."""

    model = Location
    menu_label = "Locations"
    menu_icon = "search"
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
    menu_icon = "tag"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name",)
    search_fields = ("name",)


class KeyPopAdmin(ModelAdmin):
    """Key populations admin."""

    model = KeyPopulation
    menu_label = "Key Populations"
    menu_icon = "group"
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
    menu_icon = "grip"
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
    inspect_view_enabled = True


modeladmin_register(LocationsAdmin)
modeladmin_register(TopicsAdmin)
modeladmin_register(KeyPopAdmin)
modeladmin_register(ServicesAdmin)
modeladmin_register(IssuesAdmin)
modeladmin_register(ViolationsAdmin)
modeladmin_register(PubTypesAdmin)
