import pyavagen
import io
from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.urls import reverse
from django.conf import settings
from django.db import models
from django import forms
from uuid import uuid4
from rrap.core.managers import ActiveManager
from rrap.datasets.models import Dataset
from rrap.activities.constants import ActivityTypes
from rrap.core.models import Location, Topic, KeyPopulation, Service, Issue
from wagtail.core.models import Page, PageManager
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.edit_handlers import FieldPanel, TabbedInterface, ObjectList
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailautocomplete.edit_handlers import AutocompletePanel
from wagtail.core.fields import RichTextField
from wagtail.search import index

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
        string=organization.title,
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
        ("individual", "Individual"),
        ("donor", "Donor"),
        ("government", "Government"),
        ("int_ngo", "International NGO"),
        ("cso", "Civil Society Organization"),
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

    def get_published_datasets(self):
        return Dataset.objects.filter(organization__id=self.id, status=1)

    def get_draft_datasets(self):
        return Dataset.objects.filter(organization__id=self.id, status=0)

    def get_followers(self):
        Activity = apps.get_model("activities", "Activity")
        activities = Activity.objects.select_related("from_user__profile").filter(
            organization=self, activity_type=ActivityTypes.FOLLOW
        )
        followers = []
        for activity in activities:
            followers.append(activity.from_user)
        return followers

    def get_followers_count(self):
        Activity = apps.get_model("activities", "Activity")
        followers_count = Activity.objects.filter(
            organization=self, activity_type=ActivityTypes.FOLLOW
        ).count()
        return followers_count


class OrganisationManager(PageManager):
    """custom manager to handle indexing organisations"""

    def get_index_objects(self):
        """Objects formatted for indexing"""
        return [h.dict() for h in self.get_queryset()]

    def get_filter_attributes(self):
        """A dict of filterable attributes"""
        qs = self.get_queryset()
        return {
            "services": list(set(qs.values_list("services", flat=True))),
            "issues": list(set(qs.values_list("issues", flat=True))),
        }


class OrganisationPage(Page):

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
        ("individual", "Individual"),
        ("donor", "Donor"),
        ("government", "Government"),
        ("int_ngo", "International NGO"),
        ("cso", "Civil Society Organization"),
        ("private_sector", "Private sector"),
        ("religious", "Religious"),
        ("other", "Other"),
    )

    acronym = models.CharField(max_length=10, null=True, blank=True)
    summary = models.TextField(
        max_length=240,
        null=True,
        blank=True,
        help_text="Describe organisation in one sentence.",
    )
    about = models.TextField(max_length=400, null=True, blank=True)
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    website = models.URLField(null=True, blank=True)
    locations = ParentalManyToManyField(
        Location, related_name="organisations", blank=True
    )
    topics = ParentalManyToManyField(Topic, related_name="organisations", blank=True)
    communities = ParentalManyToManyField(
        KeyPopulation, related_name="organisations", blank=True
    )
    services = ParentalManyToManyField(
        Service, related_name="organisations", blank=True
    )
    issues = ParentalManyToManyField(Issue, related_name="organisations", blank=True)
    org_type = models.CharField(
        "Type of organization",
        blank=True,
        max_length=20,
        choices=ORGANIZATION_TYPE,
    )
    status = models.SmallIntegerField(choices=ORG_STATUSES, default=0)
    email = models.EmailField("Contact Email", blank=True, null=True)
    facebook = models.URLField(
        blank=True, null=True, help_text="Your Facebook page URL"
    )
    twitter = models.URLField(
        blank=True, null=True, max_length=255, help_text="Your twitter URL"
    )
    youtube = models.URLField(
        blank=True, null=True, help_text="Your YouTube channel or user account URL"
    )
    instagram = models.URLField(
        blank=True, null=True, max_length=255, help_text="Your instagram URL"
    )
    medium = models.URLField(
        blank=True, null=True, max_length=255, help_text="Your medium page URL"
    )
    phone = models.CharField(
        blank=True, null=True, max_length=15, help_text="Telephone number"
    )
    toll_free = models.CharField(
        blank=True, null=True, max_length=20, help_text="Toll-free number"
    )
    address = RichTextField(
        blank=True, null=True, max_length=200, help_text="Office address"
    )

    objects = OrganisationManager()

    search_fields = Page.search_fields + [
        index.SearchField("title"),
        index.SearchField("summary"),
        index.SearchField("about"),
        index.SearchField("acronym"),
        index.SearchField("get_org_type_display"),
        index.FilterField("org_type"),
        index.RelatedFields("locations", [index.SearchField("name")]),
        index.RelatedFields("communities", [index.SearchField("title")]),
        index.RelatedFields("services", [index.SearchField("title")]),
        index.RelatedFields("issues", [index.SearchField("title")]),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("about"),
        FieldPanel("summary"),
        FieldPanel("acronym"),
        FieldPanel("org_type"),
        ImageChooserPanel("logo"),
    ]

    tagging_panels = [
        AutocompletePanel("locations", target_model=Location),
        FieldPanel("topics", widget=forms.CheckboxSelectMultiple),
        FieldPanel("communities", widget=forms.CheckboxSelectMultiple),
        FieldPanel("services", widget=forms.CheckboxSelectMultiple),
        FieldPanel("issues", widget=forms.CheckboxSelectMultiple),
    ]

    contact_panels = [
        FieldPanel("toll_free"),
        FieldPanel("phone"),
        FieldPanel("website"),
        FieldPanel("email"),
        FieldPanel("facebook"),
        FieldPanel("twitter"),
        FieldPanel("youtube"),
        FieldPanel("instagram"),
        FieldPanel("address"),
    ]

    settings_panels = [FieldPanel("status")] + Page.settings_panels

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Details"),
            ObjectList(tagging_panels, heading="Tagging"),
            ObjectList(contact_panels, heading="Contacts"),
            ObjectList(Page.promote_panels, heading="Meta"),
            ObjectList(settings_panels, heading="Visibility"),
        ]
    )

    class Meta:
        verbose_name = "Organisation"
        verbose_name_plural = "Organisations"

    def __str__(self):
        return self.title

    def dict(self):
        return {
            "id": str(self.id),
            "slug": str(self.slug),
            "title": str(self.title),
            "summary": self.summary,
            "toll_free": self.toll_free,
            "email": str(self.email),
            "website": self.website,
            "phone": self.phone,
            "services": {
                service["id"]: service["title"]
                for service in self.services.values("id", "title")
            },
            "issues": {
                issue["id"]: issue["title"]
                for issue in self.issues.values("id", "title")
            },
            "communities": {
                community["id"]: community["title"]
                for community in self.communities.values("id", "title")
            },
        }
