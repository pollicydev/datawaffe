import pyavagen
import io
import json
from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.conf import settings
from django.shortcuts import redirect, HttpResponseRedirect
from django.urls import reverse
from django.db import models
from django import forms
from rrap.core.managers import ActiveManager
from rrap.activities.constants import ActivityTypes
from rrap.core.models import (
    Location,
    PublicationType,
    LGBTQKeyPopulation,
    LGBTQService,
    SWKeyPopulation,
    SWService,
    PWUIDService,
)
from wagtail.core.models import Page, PageManager, Orderable
from modelcluster.fields import ParentalManyToManyField, ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    TabbedInterface,
    ObjectList,
    MultiFieldPanel,
    FieldRowPanel,
    InlinePanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtailautocomplete.edit_handlers import AutocompletePanel
from wagtail.core.fields import RichTextField
from wagtail.search import index
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

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


class OrganisationManager(PageManager):
    """custom manager to handle indexing organisations"""

    def get_index_objects(self):
        """Objects formatted for indexing"""
        return [h.dict() for h in self.get_queryset()]

    def get_filter_attributes(self):
        """A dict of filterable attributes"""
        qs = self.get_queryset()
        return {
            "communities": list(set(qs.values_list("services", flat=True))),
            "services": list(set(qs.values_list("services", flat=True))),
        }


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


class ViolenceEntry(Orderable):
    page = ParentalKey("organizations.OrganisationPage", related_name="violations")
    violation = models.ForeignKey("core.Violation", on_delete=models.CASCADE)
    occurences = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        default=0,
        help_text="How many violations of this nature did you deal with?",
    )
    period = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        default=current_year(),
        validators=[MinValueValidator(2000), max_value_current_year],
        help_text="Enter year of record",
    )

    panels = [
        FieldPanel("violation"),
        FieldPanel("occurences"),
        FieldPanel("period"),
    ]


class CommunityReach(Orderable):
    page = ParentalKey("organizations.OrganisationPage", related_name="reach")
    community = models.ForeignKey(
        "core.KeyPopulation",
        on_delete=models.CASCADE,
    )
    reach = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        default=0,
        help_text="How many people in this community did you reach?",
    )
    period = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        default=current_year(),
        validators=[MinValueValidator(2000), max_value_current_year],
        help_text="Enter year of record",
    )

    panels = [
        FieldPanel("community"),
        FieldPanel("reach"),
        FieldPanel("period"),
    ]


class OrganisationPublication(Orderable):
    page = ParentalKey(
        "organizations.OrganisationPage", related_name="org_publications"
    )
    title = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text="Title of publication (max 200 chars)",
    )
    summary = models.TextField(
        max_length=300,
        null=True,
        blank=True,
        help_text="Summarize publication in one paragraph (max 300 chars)",
    )
    thumbnail = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    pub_types = ParentalManyToManyField(
        PublicationType,
        blank=True,
        verbose_name="Publication type",
        related_name="org_publications",
    )
    publication = models.ForeignKey(
        "wagtaildocs.Document",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    year = models.PositiveSmallIntegerField(
        verbose_name="Year published",
        null=True,
        blank=True,
        default=current_year(),
        validators=[MinValueValidator(1980), max_value_current_year],
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("summary"),
        ImageChooserPanel("thumbnail"),
        DocumentChooserPanel("publication"),
        FieldRowPanel(
            [
                FieldPanel("year"),
                FieldPanel("pub_types", widget=forms.CheckboxSelectMultiple),
            ]
        ),
    ]


class OrganisationIndexPage(RoutablePageMixin, Page):
    max_count = 1

    introduction = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("introduction", classname="full"),
    ]

    subpage_types = [
        "organizations.LGBTQOrganisation",
        "organizations.SexWorkOrganisation",
        "organizations.PWUIDSOrganisation",
    ]

    # wait for filter get request for map organisations
    def get_template(self, request, *args, **kwargs):
        if request.htmx:
            return "partials/organisations_index.html"
        return "organizations/organisation_index_page.html"

    def get_context(self, request, *args, **kwargs):
        # get the filter to prevent cyclic import
        from rrap.organizations.filters import OrganisationsFilter

        context = super().get_context(request, *args, **kwargs)
        # get organisations with status 1 (active)
        organisations = (
            OrganisationPage.objects.live().public().order_by("title").filter(status=1)
        )

        org_filter = OrganisationsFilter(request.GET, queryset=organisations)

        context["organisations"] = org_filter.qs
        context["total_organisations"] = org_filter.qs.count()
        context["org_filter_form"] = org_filter.form
        context["index_url"] = self.get_url()

        return context

    def serve(self, request, view=None, args=None, kwargs=None):
        if request.user.is_authenticated:
            return super().serve(request, view, args, kwargs)
        else:
            return HttpResponseRedirect(reverse("account_login"))


class OrganisationPage(Page):

    subpage_types = []

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

    FUNDING_SOURCES = (
        ("individual", "Individual"),
        ("donor", "Donor"),
        ("government", "Government"),
        ("other", "Other"),
    )

    ORG_TYPES = (
        ("lgbtqorganisation", "LGBTQ organisation"),
        ("sexworkorganisation", "Sex workers organisation"),
        ("pwuidsorganisation", "PWUIDs organisation"),
    )

    org_type = models.CharField(
        blank=True,
        max_length=30,
        choices=ORG_TYPES,
    )

    acronym = models.CharField(max_length=10, null=True, blank=True)
    summary = models.TextField(
        max_length=240,
        null=True,
        blank=True,
        help_text="Describe organisation in one sentence.",
    )
    about = models.TextField(max_length=1000, null=True, blank=True)
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    website = models.URLField(null=True, blank=True)
    # filterables
    locations = ParentalManyToManyField(
        Location,
        related_name="organisations",
        blank=True,
        verbose_name="Where do you work? (select all districts that apply)",
    )
    funding_sources = models.CharField(
        "Funding sources",
        blank=True,
        max_length=20,
        choices=FUNDING_SOURCES,
    )
    status = models.SmallIntegerField(
        choices=ORG_STATUSES, default=1
    )  # set to active by default
    # contact information
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
        blank=True,
        null=True,
        max_length=20,
        help_text="Toll-free number",
        verbose_name="Has toll free",
    )
    address = RichTextField(
        blank=True, null=True, max_length=200, help_text="Office address"
    )

    needs_priorities = models.TextField(
        "What are the organisation's needs and priorities?",
        max_length=2000,
        null=True,
        blank=True,
        help_text="e.g. disability-specific services, mental health support, etc. Write freely. Max 2000 characters",
    )

    # PERSONNEL
    paralegals = models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    educators = models.PositiveSmallIntegerField(
        null=True, blank=True, default=0, verbose_name="Peer Educators"
    )
    village_teams = models.PositiveSmallIntegerField(
        null=True, blank=True, default=0, verbose_name="Village health teams"
    )

    # PWDs
    support_pwds = models.BooleanField(
        "Does the organisation actively support Persons with Disability(PWDs)?",
        default=True,
        blank=True,
        help_text="Check the box if Yes",
    )

    objects = OrganisationManager()

    search_fields = Page.search_fields + [
        index.SearchField("title"),
        index.SearchField("summary"),
        index.SearchField("about"),
        index.SearchField("acronym"),
        index.SearchField("get_funding_sources_display"),
        index.FilterField("funding_sources"),
        index.RelatedFields("locations", [index.SearchField("name")]),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("acronym"),
        FieldPanel("summary"),
        FieldPanel("about"),
        FieldPanel("funding_sources"),
        ImageChooserPanel("logo"),
        MultiFieldPanel(
            [
                FieldPanel("paralegals"),
                FieldPanel("educators"),
                FieldPanel("village_teams"),
            ],
            heading="Resource Personnel",
        ),
    ]

    tagging_panels = [
        AutocompletePanel("locations", target_model=Location),
        FieldPanel("support_pwds"),
        FieldPanel("needs_priorities", classname="full"),
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

    reach_panels = [
        MultiFieldPanel(
            [InlinePanel("reach", max_num=30, min_num=0, label="Reach")],
            heading="Reach within key populations",
        ),
    ]

    violations_panels = [
        MultiFieldPanel(
            [InlinePanel("violations", max_num=30, min_num=0, label="Violation")],
            heading="Record Human Rights Violations",
        ),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Info"),
            ObjectList(tagging_panels, heading="Tagging"),
            ObjectList(contact_panels, heading="Contacts"),
            ObjectList(reach_panels, heading="Reach & Impact"),
            ObjectList(violations_panels, heading="Violations"),
            ObjectList(Page.promote_panels, heading="Meta"),
            ObjectList(settings_panels, heading="Visibility"),
        ]
    )

    class Meta:
        verbose_name = "Organisation"
        verbose_name_plural = "Organisations"

    def __str__(self):
        if self.acronym:
            # e.g Uganda Key Populations Consortium-UKPC
            return "{}-{}".format(self.title, self.acronym)
        return self.title

    def list_districts(self):
        districts = self.locations.values_list("name", flat=True)
        district_list = list(districts)
        return json.dumps(district_list)

    def total_reach(self):
        if self.reach.all:
            all_reach = list(self.reach.values_list("reach", flat=True))
        else:
            all_reach = 0
        return sum(all_reach)

    def total_personnel(self):
        total = self.paralegals + self.educators
        return total

    def get_teams(self):
        return self.village_teams

    def total_violations(self):
        if self.violations.all:
            all_violations = list(self.violations.values_list("occurences", flat=True))
        else:
            all_violations = 0
        return sum(all_violations)

    def get_followers(self):
        Activity = apps.get_model("activities", "Activity")
        activities = Activity.objects.select_related("from_user__profile").filter(
            organisation=self, activity_type=ActivityTypes.FOLLOW
        )
        followers = []
        for activity in activities:
            followers.append(activity.from_user)
        return followers

    def get_followers_count(self):
        Activity = apps.get_model("activities", "Activity")
        followers_count = Activity.objects.filter(
            organisation=self, activity_type=ActivityTypes.FOLLOW
        ).count()
        return followers_count

    def serve(self, request):
        if request.user.is_authenticated:
            return super().serve(request)
        else:
            return HttpResponseRedirect(reverse("account_login"))

    def get_context(self, request):
        context = super(OrganisationPage, self).get_context(request)

        # getData for chart on reach for this organisation
        reachData = CommunityReach.objects.filter(page=self).values(
            "community", "period", "reach"
        )

        violationsData = ViolenceEntry.objects.filter(page=self).values(
            "violation", "period", "occurences"
        )

        # list of years from this dataset
        reach_years = list(
            reachData.order_by("period")
            .values_list("period", flat=True)
            .distinct()
            .reverse()
        )
        # list of key populations from this dataset
        communities = list(
            reachData.order_by("community")
            .values_list("community", flat=True)
            .distinct()
        )
        reach_data_series = {}

        for comm in communities:
            if not comm in reach_data_series:
                reach_data_series[comm] = {}
            for year in reach_years:
                reach_data_series[comm][year] = 0

        for dataset in reachData:
            comm = dataset["community"]
            year = dataset["period"]
            reach = dataset["reach"]
            reach_data_series[comm][year] = reach

        reachChartSeries = [
            {"community_id": d, "data": list(reach_data_series[d].values())}
            for d in reach_data_series
        ]

        reachPieChartSeries = [
            {"community_id": d, "data": sum(list(reach_data_series[d].values()))}
            for d in reach_data_series
        ]

        # list of years from this dataset
        violations_years = list(
            violationsData.order_by("period")
            .values_list("period", flat=True)
            .distinct()
            .reverse()
        )
        # list of key populations from this dataset
        violations = list(
            violationsData.order_by("violation")
            .values_list("violation", flat=True)
            .distinct()
        )
        violations_data_series = {}

        for violation in violations:
            if not violation in violations_data_series:
                violations_data_series[violation] = {}
            for year in violations_years:
                violations_data_series[violation][year] = 0

        for dataset in violationsData:
            violation = dataset["violation"]
            year = dataset["period"]
            occurences = dataset["occurences"]
            violations_data_series[violation][year] = occurences

        violationsChartSeries = [
            {"violation_id": d, "data": list(violations_data_series[d].values())}
            for d in violations_data_series
        ]

        violationsPieChartSeries = [
            {"violation_id": d, "data": sum(list(violations_data_series[d].values()))}
            for d in violations_data_series
        ]

        context["reachData"] = reachData.order_by("period").reverse()
        context["reach_years"] = reach_years
        context["reach_communities"] = communities
        context["reachChartSeries"] = reachChartSeries
        context["reachPieChartSeries"] = reachPieChartSeries

        context["violationsData"] = violationsData.order_by("period").reverse()
        context["violations_years"] = violations_years
        context["violationsChartSeries"] = violationsChartSeries
        context["violationsPieChartSeries"] = violationsPieChartSeries

        return context


class LGBTQOrganisation(OrganisationPage):
    """LGBTQ scoped organisation"""

    template = "organizations/lgbtq_page.html"
    parent_page_types = ["OrganisationIndexPage"]

    communities = ParentalManyToManyField(
        LGBTQKeyPopulation,
        related_name="lgbtq_organisations",
        blank=True,
        verbose_name="Key Populations Supported",
    )
    services = ParentalManyToManyField(
        LGBTQService,
        related_name="lgbtq_organisations",
        blank=True,
        verbose_name="Services Offered",
    )

    lgbt_tagging_panels = [
        FieldPanel("communities", widget=forms.CheckboxSelectMultiple),
        FieldPanel("services", widget=forms.CheckboxSelectMultiple),
    ] + OrganisationPage.tagging_panels

    edit_handler = TabbedInterface(
        [
            ObjectList(OrganisationPage.content_panels, heading="Info"),
            ObjectList(lgbt_tagging_panels, heading="Tagging"),
            ObjectList(OrganisationPage.contact_panels, heading="Contacts"),
            ObjectList(OrganisationPage.reach_panels, heading="Reach & Impact"),
            ObjectList(OrganisationPage.violations_panels, heading="Violations"),
            ObjectList(Page.promote_panels, heading="Meta"),
            ObjectList(OrganisationPage.settings_panels, heading="Visibility"),
        ]
    )

    search_fields = OrganisationPage.search_fields + [
        index.RelatedFields("communities", [index.SearchField("title")]),
        index.RelatedFields("services", [index.SearchField("title")]),
    ]

    class Meta:
        verbose_name = "LGBTQ Organisation"
        verbose_name_plural = "LGBTQ Organisations"

    def save(self, *args, **kwargs):
        self.org_type = self.org_type or "lgbtqorganisation"
        super(LGBTQOrganisation, self).save(*args, **kwargs)


class SexWorkOrganisation(OrganisationPage):
    """Sex workers scoped organisation"""

    template = "organizations/sex_workers_page.html"
    parent_page_types = ["OrganisationIndexPage"]

    AGE_RANGE = (
        ("", "N/A"),
        ("15-19", "15-19 years"),
        ("20-24", "20-24 years"),
        ("25-29", "25-29 years"),
        ("30-34", "30-34 years"),
        ("35-39", "35-39 years"),
        ("40-44", "40-44 years"),
        ("45-49", "45-49 years"),
        ("50-54", "50-54 years"),
        ("55-59", "55-59 years"),
        ("60-64", "60-64 years"),
        ("65-69", "65-69 years"),
        ("70-74", "70-74 years"),
        ("75-79", "75-79 years"),
        ("80+", "80 years and above"),
    )

    SEXWORK_TYPES = (
        ("", "N/A"),
        ("Street", "Street-based"),
        ("Brothel", "Brothel-based"),
        ("Escort", "Escort work"),
    )

    age = models.CharField(
        "Average age of members",
        max_length=30,
        choices=AGE_RANGE,
        blank=True,
        help_text="Select range that applies",
    )
    sexwork_type = models.CharField(
        "Sex work activity type",
        max_length=10,
        choices=SEXWORK_TYPES,
        blank=True,
        help_text="Types of sex work activities performed",
    )
    communities = ParentalManyToManyField(
        SWKeyPopulation,
        related_name="sw_organisations",
        blank=True,
        verbose_name="Key Populations Supported",
    )
    services = ParentalManyToManyField(
        SWService,
        related_name="sw_organisations",
        blank=True,
        verbose_name="Services Offered",
    )

    demographics_panels = [
        FieldPanel("age"),
        FieldPanel("sexwork_type"),
    ]

    sw_tagging_panels = [
        FieldPanel("communities", widget=forms.CheckboxSelectMultiple),
        FieldPanel("services", widget=forms.CheckboxSelectMultiple),
    ] + OrganisationPage.tagging_panels

    edit_handler = TabbedInterface(
        [
            ObjectList(OrganisationPage.content_panels, heading="Info"),
            ObjectList(demographics_panels, heading="Demographics"),
            ObjectList(sw_tagging_panels, heading="Tagging"),
            ObjectList(OrganisationPage.contact_panels, heading="Contacts"),
            ObjectList(OrganisationPage.reach_panels, heading="Reach & Impact"),
            ObjectList(OrganisationPage.violations_panels, heading="Violations"),
            ObjectList(Page.promote_panels, heading="Meta"),
            ObjectList(OrganisationPage.settings_panels, heading="Visibility"),
        ]
    )

    search_fields = OrganisationPage.search_fields + [
        index.RelatedFields("communities", [index.SearchField("title")]),
        index.RelatedFields("services", [index.SearchField("title")]),
    ]

    class Meta:
        verbose_name = "Sex Workers Organisation"
        verbose_name_plural = "Sex Workers Organisations"

    def save(self, *args, **kwargs):
        self.org_type = self.org_type or "sexworkorganisation"
        super(SexWorkOrganisation, self).save(*args, **kwargs)


class PWUIDSOrganisation(OrganisationPage):
    """PWUIDs scoped organisation"""

    template = "organizations/pwuids_page.html"
    parent_page_types = ["OrganisationIndexPage"]

    services = ParentalManyToManyField(
        PWUIDService,
        related_name="pwuid_organisations",
        blank=True,
        verbose_name="Services Offered",
    )

    pwuid_tagging_panels = [
        FieldPanel("services", widget=forms.CheckboxSelectMultiple),
    ] + OrganisationPage.tagging_panels

    edit_handler = TabbedInterface(
        [
            ObjectList(OrganisationPage.content_panels, heading="Info"),
            ObjectList(pwuid_tagging_panels, heading="Tagging"),
            ObjectList(OrganisationPage.contact_panels, heading="Contacts"),
            ObjectList(OrganisationPage.reach_panels, heading="Reach & Impact"),
            ObjectList(OrganisationPage.violations_panels, heading="Violations"),
            ObjectList(Page.promote_panels, heading="Meta"),
            ObjectList(OrganisationPage.settings_panels, heading="Visibility"),
        ]
    )

    search_fields = OrganisationPage.search_fields + [
        index.RelatedFields("services", [index.SearchField("title")]),
    ]

    class Meta:
        verbose_name = "PWUIDs Organisation"
        verbose_name_plural = "PWUIDs Organisations"

    def save(self, *args, **kwargs):
        self.org_type = self.org_type or "pwuidsorganisation"
        super(PWUIDSOrganisation, self).save(*args, **kwargs)
