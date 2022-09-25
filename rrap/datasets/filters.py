import django_filters
from django import forms

from django.contrib.postgres import search

from django_filters_facet import Facet, FacetedFilterSet
import django_filters

from .models import Dataset
from rrap.core.models import Location


class DatasetFilterSet(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search", label="Search")
    locations = django_filters.ModelMultipleChoiceFilter(
        queryset=Location.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Dataset
        fields = ["locations", "topics"]

    def configure_facets(self):
        self.filters["locations"].facet = Facet()
        self.filters["topics"].facet = Facet()

    def filter_search(self, queryset, name, value):
        vector = search.SearchVector("title", weight="A") + search.SearchVector(
            "summary", weight="B"
        )
        query = search.SearchQuery(value, search_type="websearch")
        return (
            queryset.annotate(
                search=vector,
                rank=search.SearchRank(vector, query),
            )
            .filter(search=query)
            .order_by("-rank")
        )
