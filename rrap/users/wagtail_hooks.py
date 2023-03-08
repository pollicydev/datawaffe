from django.conf.urls import url
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.utils import quote
from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register,
)

from wagtail.contrib.modeladmin.views import (
    IndexView,
    InstanceSpecificView,
    InspectView,
)
from wagtail.contrib.modeladmin.helpers import (
    PermissionHelper,
    ButtonHelper,
    AdminURLHelper,
)
from wagtail.admin import messages
from wagtail.core import hooks
from rrap.users.models import Profile
from .tasks import send_welcome_email, send_rejection_notice
from wagtail.users.widgets import UserListingButton

User = get_user_model()


class DataUsersPermissionHelper(PermissionHelper):
    def user_can_list(self, user):
        return True

    def user_can_create(self, user):
        return False

    def user_can_edit_obj(self, user, obj):
        return False

    def user_can_inspect_obj(self, user, obj):
        return True

    def user_can_delete_obj(self, user, obj):
        return False

    def user_can_set_status_obj(self, user, obj):
        return user.can_set_status()


class DataUsersURLHelper(AdminURLHelper):
    def _get_action_url_pattern(self, action):
        if action == "index":
            return r"^%s/%s/$" % (self.opts.app_label, "data_users")
        return r"^%s/%s/%s/$" % (self.opts.app_label, "data_users", action)

    def _get_object_specific_action_url_pattern(self, action):
        return r"^%s/%s/%s/(?P<instance_pk>[-\w]+)/$" % (
            self.opts.app_label,
            "data_users",
            action,
        )


class DataUsersButtonHelper(ButtonHelper):
    def set_status_button(
        self, pk, status, label, title, classnames_add=None, classnames_exclude=None
    ):
        if classnames_add is None:
            classnames_add = []
        if classnames_exclude is None:
            classnames_exclude = []
        classnames = self.finalise_classname(classnames_add, classnames_exclude)
        url = self.url_helper.get_action_url("set_status", quote(pk))
        url += "?status=" + status
        return {
            "url": url,
            "label": label,
            "classname": classnames,
            "title": title,
        }

    def approve_button(self, pk, classnames_add=None, classnames_exclude=None):
        if classnames_add is None:
            classnames_add = []
        if "button-secondary" in classnames_add:
            classnames_add.remove("button-secondary")
        classnames_add = ["yes"] + classnames_add
        return self.set_status_button(
            pk,
            self.model.APPROVED,
            _("approve"),
            _("Approve this user"),
            classnames_add=classnames_add,
            classnames_exclude=classnames_exclude,
        )

    def reject_button(self, pk, classnames_add=None, classnames_exclude=None):
        if classnames_add is None:
            classnames_add = []
        if "button-secondary" in classnames_add:
            classnames_add.remove("button-secondary")
        classnames_add = ["no"] + classnames_add
        return self.set_status_button(
            pk,
            self.model.REJECTED,
            _("reject"),
            _("Reject this user"),
            classnames_add=classnames_add,
            classnames_exclude=classnames_exclude,
        )

    def upgrade_button(self, pk, classnames_add=None, classnames_exclude=None):
        if classnames_add is None:
            classnames_add = []
        if "button-secondary" in classnames_add:
            classnames_add.remove("button-secondary")
        classnames_add = ["yes"] + classnames_add
        return {
            "url": f"/cms/users/{pk}/#roles",
            "label": "Upgrade to Data Entrant",
            "classname": self.finalise_classname(classnames_add, classnames_exclude),
            "title": "Assign this user to an organisation as Data Entrant",
        }

    def get_buttons_for_obj(
        self, obj, exclude=None, classnames_add=None, classnames_exclude=None
    ):
        buttons = super().get_buttons_for_obj(
            obj,
            exclude=exclude,
            classnames_add=classnames_add,
            classnames_exclude=classnames_exclude,
        )
        pk = getattr(obj, self.opts.pk.attname)
        status_buttons = []
        if obj.review_status != obj.APPROVED:
            status_buttons.append(
                self.approve_button(
                    pk,
                    classnames_add=classnames_add,
                    classnames_exclude=classnames_exclude,
                )
            )
        if obj.review_status != obj.REJECTED:
            status_buttons.append(
                self.reject_button(
                    pk,
                    classnames_add=classnames_add,
                    classnames_exclude=classnames_exclude,
                )
            )
        if not obj.review_status == obj.PENDING and obj.review_status == obj.APPROVED:
            status_buttons.append(
                self.upgrade_button(
                    pk,
                    classnames_add=classnames_add,
                    classnames_exclude=classnames_exclude,
                )
            )
        return buttons + status_buttons


def update_user_status(user, status):
    user = get_object_or_404(User, pk=user)
    if status == "approved":
        user.is_active = True
        # send welcome email
        send_welcome_email(user)
    elif status == "rejected":
        user.is_active = False
        # send rejection email
        send_rejection_notice(user)
    else:
        user.is_active = False
    user.save()


class SetStatusView(InstanceSpecificView):
    def check_action_permitted(self, user):
        # return self.permission_helper.user_can_set_status_obj(user, self.instance)
        return True

    def get(self, request, *args, **kwargs):
        status = request.GET.get("status")
        if status in dict(self.model.REVIEW_CHOICES):
            previous_status = self.instance.review_status
            self.instance.review_status = status
            self.instance.save()
            verbose_label = self.instance.get_review_status_display()
            person = self.instance.name
            if "revert" in request.GET:
                messages.success(
                    request,
                    "Reverted %s's status to %s." % (person, verbose_label),
                )
            else:
                revert_url = (
                    self.url_helper.get_action_url("set_status", self.instance_pk)
                    + "?revert&status="
                    + previous_status
                )
                messages.success(
                    request,
                    "Successfully changed %s's status to %s." % (person, verbose_label),
                    buttons=[messages.button(revert_url, _("Revert"))],
                )
            # also make user active
            update_user_status(self.instance.user_id, status)
        url = request.META.get("HTTP_REFERER")
        if url is None:
            url = (
                self.url_helper.get_action_url("index")
                + "?page_id=%s" % self.instance.page_id
            )
        return redirect(url)


class DataUsersAdmin(ModelAdmin):
    model = Profile
    menu_label = "Data Users"
    menu_icon = "group"
    menu_order = 100
    list_display = (
        # "profile_avatar",
        "profile_name",
        "profile_email",
        "country",
        "profile_status",
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
        "profile_status",
        "date_joined",
    )
    export_filename = "dw_data_users_list"
    permission_helper_class = DataUsersPermissionHelper
    button_helper_class = DataUsersButtonHelper
    url_helper_class = DataUsersURLHelper
    set_status_view_class = SetStatusView

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

    def profile_status(self, obj):
        return obj.get_review_status_display()

    def get_extra_attrs_for_field_col(self, obj, field_name):
        attrs = super().get_extra_attrs_for_field_col(obj, field_name)
        if field_name == "profile_status":
            attrs.update(
                {
                    "style": f"color: {obj.state_color()};text-transform: uppercase;",
                    "data-tag": "status-tag primary",  # how to get this inside class
                }
            )
        return attrs

    profile_name.short_description = "Name or Alias"
    profile_email.short_description = "Email address"
    profile_avatar.short_description = "Avatar"
    profile_status.short_description = "Status"
    profile_avatar.allow_tags = True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(user__is_staff=True)

    def set_status_view(self, request, instance_pk):
        kwargs = {"model_admin": self, "instance_pk": instance_pk}
        view_class = self.set_status_view_class
        return view_class.as_view(**kwargs)(request)

    def get_admin_urls_for_registration(self):
        urls = super().get_admin_urls_for_registration()
        urls += (
            url(
                self.url_helper.get_action_url_pattern("set_status"),
                self.set_status_view,
                name=self.url_helper.get_action_url_name("set_status"),
            ),
        )
        return urls


modeladmin_register(DataUsersAdmin)


@hooks.register("construct_main_menu")
def hide_some_admin_items_from_data_users(request, menu_items):
    if not request.user.is_superuser:
        menu_items[:] = [item for item in menu_items if item.label != "Data Users"]
