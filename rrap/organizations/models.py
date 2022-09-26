import pyavagen
import io
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.urls import reverse
from django.conf import settings
from django.db import models
from uuid import uuid4
from rrap.core.managers import ActiveManager
from rrap.datasets.models import Dataset
from multiselectfield import MultiSelectField

User = get_user_model()


def get_logo_full_path(instance, filename):
    ext = filename.split(".")[-1]
    path = f"{settings.MEDIA_PUBLIC_ROOT}/organizations/logos"
    name = f"{instance.id}_{instance.logo_version:04d}"
    return f"{path}/{name}.{ext}"


def generate_logo(organization):
    img_io = io.BytesIO()
    logo = pyavagen.Avatar(
        pyavagen.CHAR_SQUARE_AVATAR,
        size=500,
        string=organization.acronym,
        blur_radius=100,
    )
    logo.generate().save(img_io, format="PNG", quality=100)
    img_content = ContentFile(img_io.getvalue(), f"{organization.pk}.png")

    return img_content


def change_logo(organization, image_file):
    if organization.logo:
        organization.logo.delete()
    organization.logo_version += 1
    organization.logo = image_file
    organization.save()

    return organization


class Organization(models.Model):

    UNVERIFIED = 0
    ACTIVE = 1
    INACTIVE = 2
    DISABLED = 3
    SUSPENDED = 4
    ORG_STATUSES = (
        (ACTIVE, "Active"),
        (INACTIVE, "Inactive"),
        (UNVERIFIED, "Not verified"),
        (DISABLED, "Disabled"),
        (SUSPENDED, "Suspended"),
    )

    ORGANIZATION_TYPE = (
        ("academic", "Academic/Research"),
        ("donor", "Donor"),
        ("government", "Government"),
        ("int_ngo", "International NGO"),
        ("int_org", "International organization"),
        ("national_org", "National organization"),
        ("private_sector", "Private sector"),
        ("religious", "Religious"),
        ("other", "Other"),
    )

    name = models.SlugField("name", max_length=255)
    title = models.CharField("title", max_length=400, unique=True)
    uuid = models.UUIDField(unique=True, db_index=True, default=uuid4)
    acronym = models.CharField(max_length=10, null=True, blank=True)
    about = models.TextField(max_length=400, null=True, blank=True)
    logo = models.ImageField(upload_to=get_logo_full_path, blank=True)
    logo_version = models.IntegerField(default=0, blank=True, editable=False)
    website = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    create_date = models.DateTimeField("date created", auto_now_add=True)
    last_update = models.DateTimeField("last update", auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="owner")
    members = models.ManyToManyField(
        User, related_name="members", verbose_name="members"
    )
    locations = models.ManyToManyField("core.Location", related_name="organizations")
    org_type = models.CharField(
        "Type of organization",
        blank=True,
        max_length=20,
        choices=ORGANIZATION_TYPE,
    )
    status = models.SmallIntegerField(choices=ORG_STATUSES, default=0)

    objects = ActiveManager()

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "organizations"
        unique_together = (("name", "owner"),)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("organization", kwargs={"org_name": self.name})

    def is_owner_or_member(self, user):
        if user.id == self.owner.id:
            return True
        for member in self.members.all():
            if user.id == member.id:
                return True
        return False

    def get_datasets(self):
        return Dataset.objects.filter(organization__id=self.id)
