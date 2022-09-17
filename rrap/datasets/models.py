from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.db import models
from django.shortcuts import redirect
from django.utils import timezone
from uuid import uuid4
from taggit.managers import TaggableManager
from rrap.core.managers import ActiveManager
from .defs import get_icon_for_mime, get_alt_for_mime


User = get_user_model()


class Dataset(models.Model):
    organization = models.ForeignKey(
        "organizations.Organization", on_delete=models.CASCADE, related_name="datasets"
    )
    title = models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)
    removed = models.DateField(null=True)
    mime = models.CharField(max_length=255, null=True)
    topic = models.ForeignKey(
        "core.Topic", null=True, blank=True, on_delete=models.PROTECT
    )
    location = models.ForeignKey(
        "core.Location", null=True, blank=True, on_delete=models.PROTECT
    )
    is_active = models.BooleanField(default=True)
    uuid = models.UUIDField(unique=True, db_index=True, default=uuid4, editable=False)

    tags = TaggableManager(blank=True)
    objects = ActiveManager()

    class Meta:
        ordering = ["-date", "title"]

    def set_active(self, active):
        self.is_active = active
        if not self.is_active:
            self.removed = timezone.now().date()
        self.save()

    def delete(self, using=None, **kwargs):
        DatasetVersion.objects.filter(dataset=self).delete()
        super(Dataset, self).delete(using)

    @property
    def description(self):
        if not hasattr(self, "dataset"):
            self.dataset = self.get_latest()
        return self.dataset.description

    @property
    def user(self):
        if not hasattr(self, "dataset"):
            self.dataset = self.get_latest()
        return self.dataset.user

    @property
    def created(self):
        if not hasattr(self, "dataset"):
            self.dataset = self.get_latest()
        return self.dataset.created

    @property
    def file(self):
        if not hasattr(self, "dataset"):
            self.dataset = self.get_latest()
        return self.dataset.file

    @property
    def get_icon(self):
        if not hasattr(self, "dataset"):
            self.dataset = self.get_latest()
        return self.dataset.get_icon()

    @property
    def get_alt(self):
        if not hasattr(self, "dataset"):
            self.dataset = self.get_latest()
        return self.dataset.get_alt()

    def get_latest(self):
        return self.datasetversion_set.latest()

    def list_versions(self):
        return self.datasetversion_set.all()

    def can(self, user, _permissions):
        if user.is_superuser:
            return True
        return (
            True
            if DatasetPermission.objects.filter(
                permission__in=Permission.objects.filter(
                    codename__in=_permissions, content_type__app_label="datasets"
                ),
                user=user,
                dataset=self,
            ).exists()
            or self.project.can(user, _permissions)
            or self.project.organization.can(user, _permissions)
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
            codename=permission, content_type__app_label="datasets"
        )

        try:
            dataset_permission = DatasetPermission.objects.get(user=user, dataset=self)
            dataset_permission.permission = permission
            dataset_permission.save()
        except DatasetPermission.DoesNotExist:
            dataset_permission = DatasetPermission.objects.create(
                user=user, dataset=self, permission=permission
            )
        return dataset_permission

    def add_create(self, user):
        return self.add_permission(user, "can_create")

    def add_invite(self, user):
        return self.add_permission(user, "can_invite")

    def add_manage(self, user):
        return self.add_permission(user, "can_manage")

    def delete_permission(self, user, permission):
        try:
            DatasetPermission.objects.get(
                permission=Permission.objects.get(
                    codename=permission, content_type__app_label="datasets"
                ),
                user=user,
                dataset=self,
            ).delete()
            return True
        except DatasetPermission.DoesNotExist:
            return False

    def delete_create(self, user):
        self.delete_permission(user, "can_create")

    def delete_invite(self, user):
        self.delete_permission(user, "can_invite")

    def delete_manage(self, user):
        self.delete_permission(user, "can_manage")

    def __str__(self):
        return self.name


class DatasetVersion(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    dataset = models.ForeignKey("datasets.Dataset", null=True, on_delete=models.CASCADE)
    # This is so that the bc api can create dataset without getting the file.
    file = models.FileField(null=True, max_length=255)
    url = models.URLField(max_length=3000)
    size = models.IntegerField(default=0)
    description = models.TextField(null=True)
    created = models.DateTimeField(default=timezone.now)  # Update save method
    changed = models.DateTimeField(default=timezone.now)  # Update save method
    mime = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT
    )
    name = models.CharField(max_length=255)

    class Meta:
        get_latest_by = "created"
        ordering = ["name", "created"]

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
        save_dataset=False,
    ):
        if save_dataset:
            self.dataset.mime = self.mime
            self.dataset.save()
        super(DatasetVersion, self).save(
            force_insert, force_update, using, update_fields
        )

    def delete(self, using=None):
        if Dataset.objects.filter(pk=self.dataset.pk).count() < 1:
            self.dataset.delete()
        super(DatasetVersion, self).delete(using)

    def http_response(self):
        manager = settings.PLATFORM_MANAGER()
        url = manager.get_dataset_url(self)
        return redirect(url)

    def get_icon(self):
        return get_icon_for_mime(self.mime)

    def get_alt(self):
        return get_alt_for_mime(self.mime)

    def __str__(self):
        return self.name


class DatasetPermission(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    def __str__(self):
        return "{0} | {1} | {2}".format(
            self.dataset, self.user, self.permission.codename
        )
