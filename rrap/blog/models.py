from django import forms
from django.conf import settings
from django.core.paginator import EmptyPage, Paginator
from django.db import models
from django.db.models import Q, Count
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from modelcluster.fields import ParentalManyToManyField
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    MultiFieldPanel,
    TabbedInterface,
    ObjectList,
)
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from rrap.organizations.models import OrganisationPage
from rrap.core.models import Topic

# from rrap.blog.blocks import BlogBlocks


class BlogIndexPage(RoutablePageMixin, Page):
    max_count = 1

    introduction = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("introduction", classname="full"),
    ]

    subpage_types = ["BlogPage"]

    # Overrides the context to list all child items, that are live, by the
    # date that they were published
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        all_posts = BlogPage.objects.live().public().order_by("-date")

        page = request.GET.get("page", 1)
        try:
            page = int(page)
        except ValueError:
            page = 1

        if page == 1:
            context["latest"] = all_posts.first()
            all_posts = all_posts[1:]

        # paginate all posts by 9 per page
        paginator = Paginator(all_posts, 9)

        try:
            posts = paginator.page(page)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)  # return last page.

        context["posts"] = posts
        context["topics"] = (
            Topic.objects.live()
            .exclude(is_project=True)
            .annotate(num_blogpages=Count("blogpage"))
            .filter(num_blogpages__gt=0)
            .order_by("title")
        )
        context["blogtypes"] = BlogPageType.objects.all()

        return context

    # Create new route on the index for the topic filter
    @route(r"^topic/(?P<topic_slug>[-\w]*)/$", name="topic_view")
    def topic_view(self, request, topic_slug):
        context = self.get_context(request)

        try:
            topic = Topic.objects.get(slug=topic_slug)
        except Topic.DoesNotExist:
            return redirect(self.get_url())

        context["topic"] = topic
        posts = (
            BlogPage.objects.live()
            .public()
            .order_by("-date")
            .filter(topics__in=[topic])
        )
        context["latest"] = posts.first()
        context["posts"] = posts[1:]

        return render(request, "blog/blog_index_page.html", context)

    @route(r"^type/(?P<blogtype_slug>[-\w]*)/$", name="blogtype_view")
    def blogtype_view(self, request, blogtype_slug):
        context = self.get_context(request)

        try:
            blogtype = BlogPageType.objects.get(slug=blogtype_slug)
        except Topic.DoesNotExist:
            return redirect(self.get_url())

        context["blogtype"] = blogtype
        posts = (
            BlogPage.objects.live()
            .public()
            .order_by("-date")
            .filter(blog_page_type=blogtype)
        )
        context["latest"] = posts.first()
        context["posts"] = posts[1:]

        return render(request, "blog/blog_index_page.html", context)


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "BlogPage", related_name="tagged_items", on_delete=models.CASCADE
    )


class BlogPageType(models.Model):
    name = models.CharField(max_length=255)
    name_plural = models.CharField(max_length=255)
    slug = models.SlugField(verbose_name="slug", allow_unicode=True, max_length=255)

    panels = [
        FieldPanel("name"),
        FieldPanel("name_plural"),
        FieldPanel("slug"),
    ]

    class Meta:
        verbose_name = "Blog Page Type"
        verbose_name_plural = "Blog Page Types"
        ordering = ["name"]

    def __str__(self):
        return self.name


def limit_author_choices():
    """Limit choices in blog author field based on config settings"""
    LIMIT_AUTHOR_CHOICES = getattr(settings, "BLOG_LIMIT_AUTHOR_CHOICES_GROUP", None)
    if LIMIT_AUTHOR_CHOICES:
        if isinstance(LIMIT_AUTHOR_CHOICES, str):
            limit = Q(groups__name=LIMIT_AUTHOR_CHOICES)
        else:
            limit = Q()
            for s in LIMIT_AUTHOR_CHOICES:
                limit = limit | Q(groups__name=s)
        if getattr(settings, "BLOG_LIMIT_AUTHOR_CHOICES_ADMIN", False):
            limit = limit | Q(is_staff=True)
    else:
        limit = {"is_staff": True}
    return limit


class BlogPage(Page):
    introduction = models.TextField(help_text="Text to describe the page", blank=True)

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Landscape mode only; horizontal width between 1000px and 3000px.",
    )

    body = RichTextField(blank=True)

    date = models.DateTimeField(
        _("Post date"),
        default=timezone.now,
        help_text=_(
            "This date may be displayed on the blog post. It is not "
            "used to schedule posts to go live at a later date."
        ),
    )

    topics = ParentalManyToManyField(Topic, blank=True)
    organisations = ParentalManyToManyField(OrganisationPage, blank=True)

    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    blog_page_type = ParentalManyToManyField("blog.BlogPageType", blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("introduction", classname="full"),
        ImageChooserPanel("image"),
        StreamFieldPanel("body"),
        FieldPanel("tags"),
        FieldPanel("date"),
    ]

    tagging_panels = [
        FieldPanel("blog_page_type", widget=forms.CheckboxSelectMultiple),
        FieldPanel("topics", widget=forms.CheckboxSelectMultiple),
        FieldPanel("organisations", widget=forms.CheckboxSelectMultiple),
    ]
    settings_panels = Page.settings_panels

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(tagging_panels, heading="Topics & Community"),
            ObjectList(Page.promote_panels, heading="Promote"),
            ObjectList(settings_panels, heading="Settings", classname="settings"),
        ]
    )

    search_fields = Page.search_fields + [
        index.SearchField("introduction"),
        index.SearchField("body"),
        index.FilterField("topics"),
        index.FilterField("organisations"),
    ]

    # Specifies parent to BlogPage as being BlogIndexPages
    parent_page_types = ["BlogIndexPage"]

    # Specifies what content types can exist as children of BlogPage.
    # Empty list means that no child content types are allowed.
    subpage_types = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # TODO: Maybe actually find related posts?
        context["related_posts"] = (
            BlogPage.objects.live().public().order_by("-date").exclude(id=self.id)[:3]
        )

        return context

    def save_revision(self, *args, **kwargs):
        if not self.author:
            self.author = self.owner
        return super().save_revision(*args, **kwargs)

    # Specify featured image for meta tag

    def get_meta_image(self):
        """A relevant Wagtail Image to show. Optional."""
        return self.image

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"
        ordering = ["date", "title"]
