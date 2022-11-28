from django.db import models
from django.contrib.gis.db.models import PolygonField
from wagtail.core.models import Page
from django import forms
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel
from modelcluster.models import ClusterableModel
from wagtail_color_panel.fields import ColorField
from wagtail_color_panel.edit_handlers import NativeColorPanel


class HomePage(Page):
    template = "core/home.html"
    max_count = 1

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

        from rrap.organizations.models import OrganisationPage

        context = super().get_context(request, *args, **kwargs)
        organisations = OrganisationPage.objects.all()
        total_organisations = organisations.count()
        context["organisations"] = organisations
        context["total_organisations"] = total_organisations

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
            "title", classname="full", widget=forms.TextInput(attrs={"disabled": True})
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
