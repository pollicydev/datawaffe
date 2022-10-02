from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from uuid import uuid4
from taggit.managers import TaggableManager
from rrap.core.managers import ActiveManager
from .defs import get_icon_for_mime, get_alt_for_mime
from django.utils import timezone


User = get_user_model()


class Dataset(models.Model):

    # Status
    DRAFT = 0
    PUBLISHED = 1
    STATUS = ((DRAFT, "Draft"), (PUBLISHED, "Published"))

    # Methodology
    CENSUS = 0
    SURVEY = 1
    OBSERVATIONAL = 2
    REGISTRY = 3
    OTHER = 4
    DATA_METHODOLOGY = (
        (CENSUS, "Census"),
        (SURVEY, "Sample survey"),
        (OBSERVATIONAL, "Direct observational/Anecdotal data"),
        (REGISTRY, "Registry"),
        (OTHER, "Other"),
    )

    # Dataset update frequency
    WEEKLY = 0
    FORTNIGHTLY = 1
    MONTHLY = 2
    QUARTERLY = 3
    SEMI_ANNUALLY = 4
    ANNUALLY = 5
    AS_NEEDED = 6
    NEVER = 7
    UPDATE_FREQUENCY = (
        (WEEKLY, "Every week"),
        (FORTNIGHTLY, "Every two weeks"),
        (MONTHLY, "Every month"),
        (QUARTERLY, "Every three months"),
        (SEMI_ANNUALLY, "Every six months"),
        (ANNUALLY, "Every year"),
        (AS_NEEDED, "As needed"),
        (NEVER, "Never"),
    )

    # PRIVACY SETTING
    REQUEST = 0
    PRIVATE = 1
    PUBLIC = 2
    DATA_PRIVACY = (
        (
            REQUEST,
            "By request (Anyone can search and view the metadata of this dataset. Registered users can submit a request to obtain the data directly from you, by email, file transfer, etc.)",
        ),
        (
            PRIVATE,
            "Private (Only you and other members of your organisation can search, view/edit or download this dataset)",
        ),
        (PUBLIC, "Public (Anyone can search, view/edit or download this dataset)"),
    )

    name = models.SlugField("name", max_length=255)
    title = models.CharField("title", max_length=255, help_text="Title of dataset")
    summary = models.TextField(
        "overview",
        max_length=300,
        blank=False,
        help_text="Please provide a summary of this dataset.",
    )
    file = models.FileField(null=True, max_length=255, upload_to="datasets/")
    file_mime = models.CharField(max_length=255, null=True)
    file_url = models.URLField(null=True, blank=True)
    privacy = models.SmallIntegerField(
        "Privacy setting", blank=False, choices=DATA_PRIVACY, default=2
    )
    organization = models.ForeignKey(
        "organizations.Organization", on_delete=models.CASCADE, related_name="datasets"
    )
    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name="datasets_created",
        on_delete=models.SET_NULL,
    )
    updated_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name="datasets_updated",
        on_delete=models.SET_NULL,
    )
    start_date = models.DateTimeField(verbose_name="Start date", blank=True, null=True)
    end_date = models.DateTimeField(verbose_name="End date", blank=True, null=True)
    created = models.DateTimeField("date created", auto_now_add=True, null=True)
    last_updated = models.DateTimeField("last updated", auto_now=True, null=True)
    archived = models.BooleanField("Archived?", default=False)
    topics = models.ManyToManyField("core.Topic", blank=True, related_name="datasets")
    locations = models.ManyToManyField(
        "core.Location", blank=True, related_name="datasets"
    )
    update_frequency = models.SmallIntegerField(
        "Update frequency",
        choices=UPDATE_FREQUENCY,
        default=6,
    )
    methodology = models.SmallIntegerField(
        "Data methodology",
        choices=DATA_METHODOLOGY,
        default=1,
    )
    caveats = models.TextField(
        "Caveats/Comments", max_length=400, null=True, blank=True
    )
    uuid = models.UUIDField(unique=True, db_index=True, default=uuid4, editable=False)
    # The tag value is the canonical form of the dataset's tags
    tag_val = models.CharField(
        max_length=100, default="", blank=True, verbose_name="Spaces"
    )
    tags = TaggableManager(blank=True)
    has_pii = models.BooleanField(
        "Contains Personally Identifiable Information (PII) e.g names, phone numbers, Identification number, etc",
        default=False,
    )
    has_microdata = models.BooleanField(
        "Contains microdata e.g household survey results, disaggregated needs assessment data, etc",
        default=False,
    )
    quality_confirmed = models.BooleanField(
        "Dataset's quality has been confirmed", default=False
    )
    status = models.SmallIntegerField(
        choices=STATUS,
        default=0,
    )
    # INCREMENTALS

    # The number of views for the dataset.
    download_count = models.IntegerField(default=0, blank=True, db_index=True)
    # The number of views for the dataset.
    view_count = models.IntegerField(default=0, blank=True, db_index=True)
    # The numner of people following the dataset
    follow_count = models.IntegerField(default=0)

    objects = ActiveManager()

    class Meta:
        ordering = ["title"]

    def delete(self, using=None, **kwargs):
        Dataset.objects.filter(dataset=self).delete()
        super(Dataset, self).delete(using)

    def get_uuid(self):
        return self.uuid

    def get_icon(self):
        return get_icon_for_mime(self.file_mime)

    def get_alt(self):
        return get_alt_for_mime(self.file_mime)

    def parse_tags(self):
        return [tag.lower() for tag in self.tag_val.split(",") if tag]

    def age_in_days(self):
        delta = timezone.now() - self.created
        return delta.days

    def __str__(self):
        return self.title

    def is_request_only(self):
        if self.privacy == 0:
            return True

    def is_private(self):
        if self.privacy == 1:
            return True

    def is_public(self):
        if self.privacy == 2:
            return True

    def save(self, *args, **kwargs):
        self.tag_val = self.tag_val.replace(" ", "")
        # Default tags
        self.tag_val = self.tag_val or "tag1, tag2,"

        super(Dataset, self).save(*args, **kwargs)
