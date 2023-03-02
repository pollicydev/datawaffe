from django.db import models
from django.utils import timezone
from django.contrib.gis.db.models import PolygonField
from wagtail.core.models import Page
from django import forms
from wagtail.core.fields import RichTextField
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
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
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtailcaptcha.models import WagtailCaptchaEmailForm
from wagtail.snippets.models import register_snippet


class HomePage(Page):
    template = "core/home.html"
    max_count = 1
    subpage_types = [
        "core.StandardPage",
        "blog.BlogIndexPage",
        "organizations.OrganisationIndexPage",
        "core.PublicationsIndexPage",
        "core.ContactPage",
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

        reachData = (
            CommunityReach.objects.values("community_id")
            .annotate(total_reach=models.Sum("reach"))
            .order_by("community_id")
        )

        violationsData = (
            ViolenceEntry.objects.values("violation_id")
            .annotate(total_occurences=models.Sum("occurences"))
            .order_by("violation_id")
        )

        servicesData = (
            Service.objects.values("title")
            .annotate(total_orgs=models.Count("organisations"))
            .annotate(
                percentile=(models.F("total_orgs") / organisations.count()) * 100
            )  # percentile not working???
            .values("title", "total_orgs", "percentile")
            .order_by("id")
        )

        context["global_total_reach"] = CommunityReach.objects.aggregate(
            global_total_reach=models.Sum("reach")
        )
        context["global_total_violations"] = ViolenceEntry.objects.aggregate(
            global_total_violations=models.Sum("occurences")
        )

        context["test"] = servicesData
        context["reachData"] = reachData
        context["servicesData"] = servicesData
        context["violationsData"] = violationsData
        context["reachPieChartSeries"] = list(reachData)
        context["servicesPieChartSeries"] = list(servicesData)
        context["violationsPieChartSeries"] = list(violationsData)

        return context


class StandardPage(Page):

    introduction = models.TextField(help_text="Text to describe the page", blank=True)
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel("introduction", classname="full"),
        FieldPanel("body"),
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


@register_snippet
# specific to LGBT Organisation (repurposed)
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

    def get_total_reach(self):
        return +self.comm_reach

    class Meta:
        verbose_name = "Key Population"
        verbose_name_plural = "Key Populations"


@register_snippet
class SWKeyPopulation(ClusterableModel):
    title = models.CharField(max_length=100)
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

    def get_total_reach(self):
        return +self.comm_reach

    class Meta:
        verbose_name = "SW Key Population"
        verbose_name_plural = "SW Key Populations"


@register_snippet
# specific to LGBT Organisation (repurposed)
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


@register_snippet
class SWService(ClusterableModel):
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
        verbose_name = "SW Service"
        verbose_name_plural = "SW Services"


@register_snippet
class PWUIDService(ClusterableModel):
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
        verbose_name = "PWUID Service"
        verbose_name_plural = "PWUID Services"


@register_snippet
# specific to LGBT Organisation (repurposed)
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


@register_snippet
class SWViolation(ClusterableModel):
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
        verbose_name = "SW Violation"
        verbose_name_plural = "SW Violations"


@register_snippet
class PWUIDViolation(ClusterableModel):
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
        verbose_name = "PWUID Violation"
        verbose_name_plural = "PWUID Violations"


@register_snippet
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


class FormField(AbstractFormField):
    page = ParentalKey(
        "core.ContactPage",
        on_delete=models.CASCADE,
        related_name="form_fields",
    )


class ContactPage(WagtailCaptchaEmailForm):
    max_count = 1
    template = "core/contact_page.html"
    # This is the default path.
    # If ignored, Wagtail adds _landing.html to your template name
    landing_page_template = "core/contact_page_landing.html"

    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("intro"),
        InlinePanel("form_fields", label="Form Fields"),
        FieldPanel("thank_you_text"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("from_address", classname="col6"),
                        FieldPanel("to_address", classname="col6"),
                    ]
                ),
                FieldPanel("subject"),
            ],
            heading="Email Settings",
        ),
    ]
