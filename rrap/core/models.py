from django.db import models
from django.contrib.gis.db.models import PolygonField
from wagtail.core.models import Page

from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalManyToManyField, ParentalKey
from modelcluster.models import ClusterableModel
from .edit_handlers import ReadOnlyPanel


class HomePage(Page):
    template = "home/home_page.html"
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
        context = super().get_context(request, *args, **kwargs)
        # students = User.objects.exclude(is_staff=True).count()
        # # round off students to next 100 because semantics
        # students = students + 100 - students % 100
        # context["students"] = students

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
        FieldPanel("name", classname="full"),
        ReadOnlyPanel("geom"),
        FieldPanel("population"),
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
