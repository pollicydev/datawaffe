from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import models
from uuid import uuid4
from rrap.core.managers import ActiveManager
from rrap.datasets.models import Dataset
from multiselectfield import MultiSelectField

User = get_user_model()


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
    logo = models.ImageField(null=True, blank=True)
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
