from django import forms
import django_filters
from rrap.blog.models import BlogPageType, BlogPage
from rrap.blog.forms import BlogFilterForm
from rrap.core.models import Topic
from rrap.organizations.models import OrganisationPage


class BlogFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-sm ps-5 text-white",
                "placeholder": "Enter keyword",
            }
        ),
    )
    blog_page_type = django_filters.ModelMultipleChoiceFilter(
        queryset=BlogPageType.objects.all().order_by("name"),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "form-control",
            }
        ),
    )
    organisations = django_filters.ModelMultipleChoiceFilter(
        queryset=OrganisationPage.objects.all().order_by("title"),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "form-control",
            }
        ),
    )
    topics = django_filters.ModelMultipleChoiceFilter(
        queryset=Topic.objects.all().order_by("name"),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = BlogPage
        fields = [
            "title",
            "blog_page_type",
            "organisations",
            "topics",
        ]
        form = BlogFilterForm
