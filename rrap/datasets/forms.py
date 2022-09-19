from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, ButtonHolder, Submit, HTML
from .models import Dataset
from django_select2 import forms as s2forms
from taggit.forms import TagWidget


class NewDatasetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = [
            "title",
            "file",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            "title",
            "file",
            ButtonHolder(
                Submit("submit", "Create Dataset", css_class="btn btn-lg btn-success"),
                HTML('<a href="" class="btn btn-lg btn-default">Cancel</a>'),
            ),
        )


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
        required=False,
        help_text="What type of data is included in this dataset. Provide a brief summary",
    )
    caveats = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        required=False,
        help_text="Add some private caveats/notes/comments about this dataset",
    )
    start_date = forms.DateTimeField(
        input_formats=["%d/%m/%Y %H:%M"],
        widget=forms.DateTimeInput(
            format="%d-%m-%Y %H:%M",
            attrs={
                "class": "form-control flatpickr-input",
                "placeholder": "Pike a date",
                "data-toggle": "flatpickr",
                "data-enable-time": "true",
                "data-date-format": "d-m-Y H:i",
            },
        ),
        label="Start date for this dataset",
        required=False,
    )
    end_date = forms.DateTimeField(
        input_formats=["%d/%m/%Y %H:%M"],
        widget=forms.DateTimeInput(
            format="%d-%m-%Y %H:%M",
            attrs={
                "class": "form-control flatpickr-input",
                "placeholder": "Pike a date",
                "data-toggle": "flatpickr",
                "data-enable-time": "true",
                "data-date-format": "d-m-Y H:i",
            },
        ),
        label="End date for this dataset",
        required=False,
    )

    class Meta:
        model = Dataset
        fields = [
            "title",
            "summary",
            "file_mime",
            "privacy",
            "update_frequency",
            "methodology",
            "start_date",
            "end_date",
            "ongoing",
            "locations",
            "topics",
            "caveats",
            "tags",
            "has_pii",
            "has_microdata",
            "quality_confirmed",
            "caveats",
            "tags",
        ]
        widgets = {
            "locations": s2forms.Select2MultipleWidget(
                attrs={
                    "class": "form-control",
                    "placeholder": "Select district(s)",
                    "data-toggle": "select2",
                    "data-placeholder": "Select district(s)",
                    "data-select2-id": "id_locations",
                }
            ),
            "topics": s2forms.Select2MultipleWidget(
                attrs={
                    "class": "form-control",
                    "placeholder": "Select topic(s)",
                    "data-toggle": "select2",
                    "data-placeholder": "Select topic(s)",
                    "data-select2-id": "id_topics",
                }
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
                    "class": "form-control",
                },
            ),
            "methodology": forms.Select(
                choices=Dataset.DATA_METHODOLOGY,
                attrs={
                    "class": "form-control",
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
                Column("ongoing", css_class="col-md-4"),
                css_class="form-group",
            ),
            HTML(
                """
                <hr>
                """
            ),
            Row(
                Column("methodology", css_class="col-md-6"),
                Column("update_frequency", css_class="col-md-6"),
            ),
            "locations",
            "topics",
            "tags",
            "caveats",
            ButtonHolder(
                Submit("submit", "Save dataset", css_class="btn btn-lg btn-success"),
                HTML('<a href="" class="btn btn-lg btn-secondary">Cancel</a>'),
            ),
        )
