from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property

from rrap.organizations.models import Organization


class OrganizationMixin:
    """
    This mixin is usually used together with a view that inherits from
    ContextMixin.
    """

    @cached_property
    def organization(self):
        queryset = Organization.objects.select_related(
            "owner__profile"
        ).prefetch_related("members__profile")
        return get_object_or_404(
            queryset,
            name=self.kwargs.get("org_name"),
        )

    def get_context_data(self, **kwargs):
        kwargs.update(organization=self.organization)
        return super().get_context_data(**kwargs)


class MainOwnerRequiredMixin(UserPassesTestMixin):
    """
    This mixin depends on having a organization property on the view class.
    It is usually used together with the OrganizationMixin
    """

    def test_func(self):
        return self.organization.owner == self.request.user


class OwnerRequiredMixin(UserPassesTestMixin):
    """
    This mixin depends on having a organization property on the view class.
    It is usually used together with the OrganizationMixin
    """

    def test_func(self):
        return self.organization.is_owner_or_member(self.request.user)
