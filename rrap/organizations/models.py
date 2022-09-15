from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.db import models
from uuid import uuid4
from rrap.core.managers import ActiveManager

# from projects.models import Project

import datetime

User = get_user_model()


class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    uuid = models.UUIDField(unique=True, db_index=True, default=uuid4)
    acronym = models.CharField(max_length=10, null=True, blank=True)
    description = models.TextField(max_length=400, null=True, blank=True)
    logo = models.ImageField(null=True, blank=True)
    removed = models.DateField(null=True)
    website = models.URLField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    objects = ActiveManager()

    class Meta:
        ordering = ["name"]

    # def set_active(self, active):
    #     self.is_active = active
    #     for person in self.user_set.all():
    #         person.set_active(active)

    #     for project in Project.objects.filter(organization=self):
    #         project.set_active(active)

    #     if not self.is_active:
    #         self.removed = datetime.date.today()
    #     self.save()

    # def get_dataset(self, user):
    #     if user.is_superuser:
    #         return Project.objects.active().filter(organization=self)
    #     else:
    #         return Project.objects.active().filter(id__in=user.get_projects().values_list('id', flat=True), organization=self)

    def __str__(self):
        return self.name

    def can(self, user, _permissions):
        if user.is_superuser:
            return True

        return (
            True
            if OrganizationPermission.objects.filter(
                permission__in=Permission.objects.filter(
                    codename__in=_permissions, content_type__app_label="organizations"
                ),
                user=user,
                organization=self,
            ).exists()
            else False
        )

    def can_create(self, user):
        return self.can(user, ["can_create", "can_invite", "can_manage"])

    def can_invite(self, user):
        return self.can(user, ["can_invite", "can_manage"])

    def can_manage(self, user):
        return self.can(user, ["can_manage"])

    def add_permission(self, user, permission):
        permission = Permission.objects.get(
            codename=permission, content_type__app_label="organizations"
        )

        try:
            organization_permission = OrganizationPermission.objects.get(
                user=user, organization=self
            )
            organization_permission.permission = permission
            organization_permission.save()
        except OrganizationPermission.DoesNotExist:
            organization_permission = OrganizationPermission.objects.create(
                user=user, organization=self, permission=permission
            )
        return organization_permission

    def add_create(self, user):
        return self.add_permission(user, "can_create")

    def add_invite(self, user):
        return self.add_permission(user, "can_invite")

    def add_manage(self, user):
        return self.add_permission(user, "can_manage")

    def delete_permission(self, user, permission):
        try:
            OrganizationPermission.objects.get(
                permission=Permission.objects.get(
                    codename=permission, content_type__app_label="organizations"
                ),
                user=user,
                organization=self,
            ).delete()
        except OrganizationPermission.DoesNotExist:
            return False

    def delete_create(self, user):
        self.delete_permission(user, "can_create")

    def delete_invite(self, user):
        self.delete_permission(user, "can_invite")

    def delete_manage(self, user):
        self.delete_permission(user, "can_manage")


class OrganizationPermission(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    def __str__(self):  # pragma: no cover
        return "{0} | {1} | {2}".format(
            self.organization, self.user, self.permission.codename
        )
