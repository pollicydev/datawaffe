from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)
from .models import Location, Topic, KeyPopulation, Service, Issue


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


modeladmin_register(LocationsAdmin)
modeladmin_register(TopicsAdmin)
modeladmin_register(KeyPopAdmin)
modeladmin_register(ServicesAdmin)
modeladmin_register(IssuesAdmin)
