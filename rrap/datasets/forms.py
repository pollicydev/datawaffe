from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, ButtonHolder, Submit, HTML, Div
from crispy_forms.bootstrap import InlineRadios
from .models import Dataset
from django_select2 import forms as s2forms


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

    class Meta:
        model = Dataset
        fields = [
            "title",
            "summary",
            "file",
            "mime",
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
        }
        labels = {
            "locations": "Select all the districts in Uganda where this project operates"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            "file",
            Row(
                Column("title", css_class="col-md-8"),
                Column("mime", css_class="col-md-4"),
                css_class="form-group",
            ),
            "summary",
            "privacy",
            "methodology",
            "update_frequency",
            "locations",
            "topics",
            "has_pii",
            "has_microdata",
            "quality_confirmed",
            Row(
                Column("start_date", css_class="col-md-4"),
                Column("end_date", css_class="col-md-4"),
                Column("ongoing", css_class="col-md-4"),
                css_class="form-group",
            ),
            ButtonHolder(
                Submit("submit", "Save dataset", css_class="btn btn-lg btn-success"),
                HTML('<a href="" class="btn btn-lg btn-secondary">Cancel</a>'),
            ),
        )
