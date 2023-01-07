from django.db import models
from django.utils import timezone
from django.contrib.gis.db.models import PolygonField
from wagtail.core.models import Page
from django import forms
from wagtail.core.fields import RichTextField
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    RichTextFieldPanel,
    FieldRowPanel,
    TabbedInterface,
    ObjectList,
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalManyToManyField, ParentalKey
from wagtail_color_panel.fields import ColorField
from wagtail_color_panel.edit_handlers import NativeColorPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.search import index


class HomePage(Page):
    template = "core/home.html"
    max_count = 1
    subpage_types = [
        "blog.BlogIndexPage",
        "organizations.OrganisationIndexPage",
        "core.PublicationsIndexPage",
    ]

    hero_heading = models.CharField(max_length=100, null=True, blank=True)
    hero_desc = models.CharField(max_length=255, null=True, blank=True)
    hero_img = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Choose feature image",
        verbose_name="Hero Image",
    )
    promo_video = models.URLField(
        blank=True,
        null=True,
        verbose_name="Intro/Promo video",
        help_text="Enter link to youtube embed here",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_heading"),
                FieldPanel("hero_desc"),
                ImageChooserPanel("hero_img"),
                FieldPanel("promo_video"),
            ],
            heading="Hero Section",
        )
    ]

    def get_context(self, request, *args, **kwargs):

        from rrap.blog.models import BlogIndexPage, BlogPage
        from rrap.organizations.models import (
            OrganisationPage,
            CommunityReach,
            ViolenceEntry,
        )
        from rrap.core.models import KeyPopulation, Location, Service

        context = super().get_context(request, *args, **kwargs)

        blogs = BlogPage.objects.live().public().order_by("-date")[:5]

        organisations = (
            OrganisationPage.objects.live().public().order_by("-first_published_at")
        )

        context["first_orgs"] = organisations[10:]
        context["last_orgs"] = organisations[:10]

        context["publications"] = (
            PublicationPage.objects.live().public().order_by("-date_published")
        )

        context["communities"] = KeyPopulation.objects.all()

        # should return only four out of the initial 5
        context["latest_article"] = blogs.first()

        context["other_articles"] = blogs[1:]

        context["indexpages"] = {
            "blog": BlogIndexPage.objects.first().get_url(),
            "publications": PublicationsIndexPage.objects.first().get_url(),
        }

        context["orgs_w_tollfree"] = OrganisationPage.objects.exclude(
            toll_free__isnull=True
        )

        used_locations = organisations.values_list("locations", flat=True).distinct()

        districts = Location.objects.filter(id__in=used_locations)

        total_districts_in_ug = Location.objects.all().count()

        context["districts"] = districts

        context["percent_districts"] = round(
            (districts.count() / total_districts_in_ug) * 100
        )

        # getData for chart on reach for this organisation
        reachData = CommunityReach.objects.values("community", "period", "reach")

        violationsData = ViolenceEntry.objects.values(
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


class StandardPage(Page):

    introduction = models.TextField(help_text="Text to describe the page", blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Landscape mode only; horizontal width between 1000px and 3000px.",
    )
    video_id = models.CharField(max_length=15, null=True, blank=True)
    cta_link = models.URLField(blank=True, null=True)
    cta_text = models.CharField(max_length=25, blank=True, null=True)
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel("introduction", classname="full"),
        FieldPanel("body"),
        ImageChooserPanel("image"),
        FieldPanel("video_id"),
        MultiFieldPanel(
            [
                FieldPanel("cta_text"),
                FieldPanel("cta_link"),
            ],
            heading="Call to Action",
        ),
    ]


# used Location as identifier but initially represents districts. Could scale to have counties and subcounties
class Location(ClusterableModel):
    name = models.CharField(max_length=100)
    geom = PolygonField(srid=4326)
    population = models.CharField(max_length=10)

    autocomplete_search_field = "name"

    panels = [
        FieldPanel(
            "name", classname="full", widget=forms.TextInput(attrs={"disabled": True})
        ),
        FieldPanel("population", widget=forms.TextInput(attrs={"disabled": True})),
    ]

    def __str__(self):
        return self.name

    def autocomplete_label(self):
        return self.name

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"


class Topic(ClusterableModel):
    name = models.CharField(max_length=100)

    autocomplete_search_field = "name"

    panels = [
        FieldPanel("name", classname="full"),
    ]

    def __str__(self):
        return self.name

    def autocomplete_label(self):
        return self.name

    class Meta:
        verbose_name = "Topic"
        verbose_name_plural = "Topics"


class KeyPopulation(ClusterableModel):
    title = models.CharField(max_length=100)
    acronym = models.CharField(max_length=10, blank=True, null=True)
    color = ColorField(default="#000000")

    panels = [
        FieldPanel(
            "title",
            classname="full",
        ),
        NativeColorPanel("color"),
    ]

    def __str__(self):
        return self.title

    def autocomplete_label(self):
        return self.title

    class Meta:
        verbose_name = "Key Population"
        verbose_name_plural = "Key Populations"


class Service(ClusterableModel):
    title = models.CharField(max_length=100, help_text="Name/title of service")
    icon = models.CharField(
        max_length=20, blank=True, null=True, help_text="Enter name of icon"
    )
    summary = models.CharField(
        max_length=240, blank=True, null=True, help_text="Describe the service"
    )

    panels = [
        FieldPanel(
            "title", classname="full", widget=forms.TextInput(attrs={"disabled": True})
        ),
        FieldPanel("summary"),
        FieldPanel("icon"),
    ]

    def __str__(self):
        return self.title

    def autocomplete_label(self):
        return self.title

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"


class Issue(ClusterableModel):
    title = models.CharField(max_length=100, help_text="Name/title of issue")
    icon = models.CharField(
        max_length=20, blank=True, null=True, help_text="Enter name of icon"
    )
    summary = models.CharField(
        max_length=240, blank=True, null=True, help_text="Describe the issue"
    )

    panels = [
        FieldPanel(
            "title", classname="full", widget=forms.TextInput(attrs={"disabled": True})
        ),
        FieldPanel("summary"),
        FieldPanel("icon"),
    ]

    def __str__(self):
        return self.title

    def autocomplete_label(self):
        return self.title

    class Meta:
        verbose_name = "Issue"
        verbose_name_plural = "Issues"


class Violation(ClusterableModel):
    title = models.CharField(max_length=100, help_text="Name of violation")
    description = models.CharField(
        max_length=240, blank=True, null=True, help_text="Brief description"
    )
    color = ColorField(default="#000000", null=True)

    panels = [
        FieldPanel("title", classname="full"),
        FieldPanel("description"),
        NativeColorPanel("color"),
    ]

    def __str__(self):
        return self.title

    def autocomplete_label(self):
        return self.title

    class Meta:
        verbose_name = "Violation"
        verbose_name_plural = "Violations"


class PublicationType(ClusterableModel):
    name = models.CharField(max_length=100)

    panels = [
        FieldPanel("name", classname="full"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Publication type"
        verbose_name_plural = "Publication types"


class PublicationsIndexPage(RoutablePageMixin, Page):
    max_count = 1
    template = "core/publications.html"

    introduction = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("introduction", classname="full"),
    ]

    subpage_types = ["PublicationPage"]

    # wait for filter get request for map organisations
    def get_template(self, request, *args, **kwargs):
        if request.htmx:
            return "partials/publications.html"
        return "core/publications.html"

    def get_context(self, request, *args, **kwargs):
        # get the filter to prevent cyclic import
        from rrap.core.filters import PublicationsFilter

        context = super().get_context(request, *args, **kwargs)
        publications = (
            PublicationPage.objects.live().descendant_of(self).order_by("title")
        )
        pub_filter = PublicationsFilter(request.GET, queryset=publications)

        context["publications"] = pub_filter.qs
        context["pub_filter_form"] = pub_filter.form
        context["index_url"] = self.get_url()

        return context


class PublicationTag(TaggedItemBase):
    content_object = ParentalKey(
        "PublicationPage", related_name="tagged_items", on_delete=models.CASCADE
    )


class PublicationPage(Page):

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

    summary = models.TextField(help_text="Text to describe the publication", blank=True)

    thumbnail = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Portrait mode only",
    )

    body = RichTextField(blank=True)

    date_published = models.DateTimeField(
        "Date of publishing",
        default=timezone.now,
        help_text=_(
            "This is the date shown publicly as the date of publishing. Only month and year will be shown though"
        ),
    )
    organisations = ParentalManyToManyField(
        "organizations.OrganisationPage", blank=True
    )
    topics = ParentalManyToManyField(Topic, blank=True)
    pub_types = ParentalManyToManyField(
        PublicationType,
        blank=True,
        verbose_name="Publication type",
        related_name="publications",
    )
    file = models.ForeignKey(
        "wagtaildocs.Document",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    tags = ClusterTaggableManager(through=PublicationTag, blank=True)

    privacy = models.SmallIntegerField(
        "Privacy setting", blank=False, choices=DATA_PRIVACY, default=2
    )

    has_pii = models.BooleanField(
        "Contains Personally Identifiable Information (PII) e.g names, phone numbers, Identification number, etc",
        default=False,
    )
    has_microdata = models.BooleanField(
        "Contains microdata e.g household survey results, disaggregated needs assessment data, etc",
        default=False,
    )

    content_panels = Page.content_panels + [
        FieldPanel("summary", classname="full"),
        ImageChooserPanel("thumbnail"),
        DocumentChooserPanel("file"),
        RichTextFieldPanel("body"),
        FieldPanel("tags"),
        FieldPanel("date_published"),
    ]

    tagging_panels = [
        FieldPanel("privacy"),
        FieldPanel("has_pii"),
        FieldPanel("has_microdata"),
        FieldPanel("pub_types", widget=forms.CheckboxSelectMultiple),
        FieldPanel("topics", widget=forms.CheckboxSelectMultiple),
        FieldPanel("organisations", widget=forms.CheckboxSelectMultiple),
    ]
    settings_panels = Page.settings_panels

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Info"),
            ObjectList(tagging_panels, heading="Tagging"),
            ObjectList(Page.promote_panels, heading="Promote"),
            ObjectList(settings_panels, heading="Settings", classname="settings"),
        ]
    )

    search_fields = Page.search_fields + [
        index.SearchField("summary"),
        index.SearchField("body"),
        index.FilterField("topics"),
        index.FilterField("organisations"),
    ]

    parent_page_types = ["PublicationsIndexPage"]

    subpage_types = []

    def __str__(self):
        return self.title

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # TODO: Maybe actually find related posts?
        context["related_publications"] = (
            PublicationPage.objects.live()
            .public()
            .order_by("-date_published")
            .exclude(id=self.id)[:3]
        )

        return context

    # Specify featured image for meta tag

    def get_meta_image(self):
        """A relevant Wagtail Image to show. Optional."""
        return self.image

    class Meta:
        verbose_name = "Publication"
        verbose_name_plural = "Publications"
        ordering = ["title", "date_published"]
