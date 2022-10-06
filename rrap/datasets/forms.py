from django import forms
from datetime import date
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, ButtonHolder, Submit, HTML
from crispy_forms.bootstrap import InlineRadios
from ..utils.widgets import BootstrapDateTimePickerInput
from .models import Dataset
from taggit.forms import TagWidget


class DatasetForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Title of dataset",
            }
        ),
        max_length=255,
        help_text="Add a descriptive title",
    )
    summary = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        required=True,
        help_text="What type of data is included in this dataset. Provide a brief summary",
    )
    caveats = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        required=False,
        help_text="Add some private caveats/notes/comments about this dataset",
    )
    start_date = forms.DateField(
        input_formats=["%Y-%m-%d"],
        initial=date.today,
        widget=BootstrapDateTimePickerInput(
            attrs={
                "class": "form-control",
                "placeholder": "Start date",
            },
        ),
        label="Start date",
        required=False,
    )
    end_date = forms.DateField(
        input_formats=["%Y-%m-%d"],
        initial=date.today,
        widget=BootstrapDateTimePickerInput(
            attrs={
                "class": "form-control",
                "placeholder": "End date",
            },
        ),
        label="End date",
        required=False,
    )

    class Meta:
        model = Dataset
        fields = [
            "title",
            "summary",
            "privacy",
            "update_frequency",
            "methodology",
            "start_date",
            "end_date",
            "locations",
            "topics",
            "caveats",
            "tags",
            "has_pii",
            "has_microdata",
            "quality_confirmed",
            "caveats",
            "tags",
            "status",
            "doc_type",
        ]
        widgets = {
            "locations": forms.SelectMultiple(
                attrs={"class": "form-control selector", "multiple": ""}
            ),
            "topics": forms.SelectMultiple(
                attrs={"class": "form-control selector", "multiple": ""}
            ),
            "privacy": forms.RadioSelect(
                choices=Dataset.DATA_PRIVACY,
                attrs={
                    "class": "form-control",
                },
            ),
            "doc_type": forms.Select(
                choices=Dataset.DOCUMENT_TYPE,
                attrs={
                    "class": "form-control selector",
                },
            ),
            "update_frequency": forms.Select(
                choices=Dataset.UPDATE_FREQUENCY,
                attrs={
                    "class": "form-control selector",
                },
            ),
            "methodology": forms.Select(
                choices=Dataset.DATA_METHODOLOGY,
                attrs={
                    "class": "form-control selector",
                },
            ),
            "tags": TagWidget(
                attrs={
                    "class": "form-control",
                }
            ),
        }
        labels = {
            "locations": "Select all the districts in Uganda for which this dataset is relevant"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            "title",
            "summary",
            "has_pii",
            "has_microdata",
            "quality_confirmed",
            HTML(
                """
                <hr>
                """
            ),
            "privacy",
            HTML(
                """
                <hr>
                """
            ),
            Row(
                Column("start_date", css_class="col-md-4"),
                Column("end_date", css_class="col-md-4"),
                Column("update_frequency", css_class="col-md-4"),
                css_class="form-group",
            ),
            HTML(
                """
                <hr>
                """
            ),
            Row(
                Column("doc_type", css_class="col-md-6"),
                Column("methodology", css_class="col-md-6"),
            ),
            "locations",
            "topics",
            "tags",
            "caveats",
            InlineRadios("status"),
            Submit("submit", "Save dataset", css_class="btn btn-lg btn-success"),
        )


class EditDatasetForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Title of dataset",
            }
        ),
        max_length=255,
        help_text="Add a descriptive title",
    )
    summary = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        required=True,
        help_text="What type of data is included in this dataset. Provide a brief summary",
    )
    caveats = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        required=False,
        help_text="Add some private caveats/notes/comments about this dataset",
    )
    start_date = forms.DateField(
        input_formats=["%d-%m-%Y"],
        initial=date.today,
        widget=BootstrapDateTimePickerInput(
            attrs={
                "class": "form-control",
                "placeholder": "Start date",
            },
            format=["%d-%m-%Y"],
        ),
        label="Start date",
        required=False,
    )
    end_date = forms.DateField(
        input_formats=["%d-%m-%Y"],
        initial=date.today,
        widget=BootstrapDateTimePickerInput(
            attrs={
                "class": "form-control",
                "placeholder": "End date",
            },
            format=["%d-%m-%Y"],
        ),
        label="End date",
        required=False,
    )

    class Meta:
        model = Dataset
        fields = [
            "title",
            "summary",
            "privacy",
            "update_frequency",
            "methodology",
            "start_date",
            "end_date",
            "locations",
            "topics",
            "caveats",
            "tags",
            "has_pii",
            "has_microdata",
            "quality_confirmed",
            "caveats",
            "tags",
            "status",
            "doc_type",
        ]
        widgets = {
            "locations": forms.SelectMultiple(
                attrs={"class": "form-control selector", "multiple": ""}
            ),
            "topics": forms.SelectMultiple(
                attrs={"class": "form-control selector", "multiple": ""}
            ),
            "doc_type": forms.Select(
                choices=Dataset.DOCUMENT_TYPE,
                attrs={
                    "class": "form-control selector",
                },
            ),
            "privacy": forms.RadioSelect(
                choices=Dataset.DATA_PRIVACY,
                attrs={
                    "class": "form-control",
                },
            ),
            "update_frequency": forms.Select(
                choices=Dataset.UPDATE_FREQUENCY,
                attrs={
                    "class": "form-control selector",
                },
            ),
            "methodology": forms.Select(
                choices=Dataset.DATA_METHODOLOGY,
                attrs={
                    "class": "form-control selector",
                },
            ),
            "tags": TagWidget(
                attrs={
                    "class": "form-control",
                }
            ),
            "status": forms.RadioSelect(
                choices=Dataset.STATUS,
                attrs={
                    "class": "form-control",
                },
            ),
        }
        labels = {
            "locations": "Select all the districts in Uganda for which this dataset is relevant"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            "title",
            "summary",
            "has_pii",
            "has_microdata",
            "quality_confirmed",
            HTML(
                """
                <hr>
                """
            ),
            "privacy",
            HTML(
                """
                <hr>
                """
            ),
            Row(
                Column("start_date", css_class="col-md-4"),
                Column("end_date", css_class="col-md-4"),
                Column("update_frequency", css_class="col-md-4"),
                css_class="form-group",
            ),
            HTML(
                """
                <hr>
                """
            ),
            Row(
                Column("doc_type", css_class="col-md-6"),
                Column("methodology", css_class="col-md-6"),
            ),
            "locations",
            "topics",
            "tags",
            "caveats",
            InlineRadios("status"),
            Submit("submit", "Update dataset", css_class="btn btn-lg btn-success"),
        )
