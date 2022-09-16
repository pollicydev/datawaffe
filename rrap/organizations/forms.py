from django import forms
from .models import Organization
from django_select2 import forms as s2forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, ButtonHolder, Submit, HTML


class CreateOrganizationForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Name of organization",
            }
        ),
        max_length=255,
    )
    about = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Write a brief summary of the work at your organization",
            }
        ),
        max_length=500,
        help_text="Try to keep it short, max 500 characters :)",
        required=False,
    )

    class Meta:
        model = Organization
        fields = [
            "title",
            "acronym",
            "about",
            "logo",
            "locations",
            "website",
        ]
        widgets = {
            "locations": s2forms.Select2MultipleWidget(
                attrs={
                    "class": "form-control form-control-lg select2-hidden-accessible",
                    "placeholder": "Select a district",
                    "data-toggle": "select2",
                    "data-placeholder": "Select a district",
                    "data-select2-id": "id_locations",
                }
            ),
            "website": forms.TextInput(attrs={"class": "form-control form-control-lg"}),
        }
        labels = {"locations": "Select all the districts in Uganda where you operate"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            "title",
            "acronym",
            "about",
            "logo",
            "locations",
            "website",
            ButtonHolder(
                Submit(
                    "submit", "Create Organisation", css_class="btn btn-md btn-success"
                ),
                HTML('<a href="" class="btn btn-default">Cancel</a>'),
            ),
        )


class OrganizationForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control form-control-lg"}),
        max_length=255,
    )
    about = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control expanding", "rows": "4"}),
        max_length=500,
        required=False,
    )

    class Meta:
        model = Organization
        fields = [
            "title",
            "acronym",
            "about",
            "logo",
            "locations",
            "website",
        ]
        widgets = {
            "locations": s2forms.Select2MultipleWidget(
                attrs={
                    "class": "form-control form-control-lg select2-hidden-accessible",
                    "placeholder": "Select a district",
                    "data-toggle": "select2",
                    "data-placeholder": "Select a district",
                    "data-select2-id": "id_locations",
                }
            ),
            "website": forms.TextInput(attrs={"class": "form-control form-control-lg"}),
        }
        labels = {"districts": "Select all the districts in Uganda where you operate"}
