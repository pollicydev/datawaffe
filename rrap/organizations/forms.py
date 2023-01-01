from django import forms
from .models import Organization, generate_logo
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, ButtonHolder, Submit, HTML
from rrap.organizations.models import OrganisationPage


class CreateOrganizationForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Name of organization",
            }
        ),
        max_length=255,
    )
    acronym = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        max_length=10,
    )
    about = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": "3",
                "placeholder": "Write a brief summary of the work at your organization",
            }
        ),
        max_length=300,
        help_text="Try to keep it short, max 300 characters :)",
        required=False,
    )

    class Meta:
        model = Organization
        fields = [
            "title",
            "org_type",
            "acronym",
            "about",
            "logo",
            "locations",
            "website",
        ]
        widgets = {
            "locations": forms.SelectMultiple(
                attrs={"class": "form-control selector", "multiple": ""}
            ),
            "org_type": forms.Select(
                choices=Organization.ORGANIZATION_TYPE,
                attrs={
                    "class": "form-control selector",
                },
            ),
            "website": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {"locations": "Select all the districts in Uganda where you operate"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            "logo",
            Row(
                Column("title", css_class="col-md-6"),
                Column("acronym", css_class="col-md-3"),
                Column("org_type", css_class="col-md-3"),
            ),
            "about",
            "locations",
            "website",
            ButtonHolder(
                Submit(
                    "submit",
                    "Request organization",
                    css_class="btn btn-lg btn-md btn-success",
                ),
                HTML('<a href="" class="btn btn-default">Cancel</a>'),
            ),
        )


class OrganizationForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control form-control-lg"}),
        max_length=255,
    )
    acronym = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        max_length=10,
    )
    about = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control expanding", "rows": "3"}),
        max_length=500,
        required=False,
    )

    class Meta:
        model = Organization
        fields = [
            "title",
            "acronym",
            "org_type",
            "about",
            "logo",
            "locations",
            "website",
        ]
        widgets = {
            "locations": forms.SelectMultiple(
                attrs={"class": "form-control selector", "multiple": ""}
            ),
            "org_type": forms.Select(
                choices=Organization.ORGANIZATION_TYPE,
                attrs={
                    "class": "form-control selector",
                },
            ),
            "website": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {"districts": "Select all the districts in Uganda where you operate"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            "logo",
            Row(
                Column("title", css_class="col-md-6"),
                Column("acronym", css_class="col-md-3"),
                Column("org_type", css_class="col-md-3"),
            ),
            "about",
            "locations",
            "website",
            ButtonHolder(
                Submit(
                    "submit",
                    "Request organization",
                    css_class="btn btn-lg btn-md btn-success",
                ),
                HTML('<a href="" class="btn btn-default">Cancel</a>'),
            ),
        )


class EditOrganizationForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        max_length=255,
    )
    acronym = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        max_length=10,
    )
    about = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control expanding", "rows": "3"}),
        max_length=500,
        required=False,
    )

    class Meta:
        model = Organization
        fields = [
            "title",
            "acronym",
            "org_type",
            "about",
            "logo",
            "locations",
            "website",
        ]
        widgets = {
            "locations": forms.SelectMultiple(
                attrs={"class": "form-control selector", "multiple": ""}
            ),
            "org_type": forms.Select(
                choices=Organization.ORGANIZATION_TYPE,
                attrs={
                    "class": "form-control selector",
                },
            ),
            "website": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {"districts": "Select all the districts in Uganda where you operate"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            "logo",
            Row(
                Column("title", css_class="col-md-6"),
                Column("acronym", css_class="col-md-3"),
                Column("org_type", css_class="col-md-3"),
            ),
            "about",
            "locations",
            "website",
            ButtonHolder(
                Submit(
                    "submit",
                    "Update organization",
                    css_class="btn btn-lg btn-md btn-success",
                ),
                HTML('<a href="" class="btn btn-default">Cancel</a>'),
            ),
        )


class OrganizationSettingsForm(forms.ModelForm):
    name = forms.SlugField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="URL",
        help_text="Only letters, numbers, underscores or hyphens are allowed.",
        max_length=255,
    )

    class Meta:
        model = Organization
        fields = [
            "name",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            "name",
            Submit(
                "submit",
                "Update slug",
                css_class="btn btn-lg btn-success",
            ),
        )


class DeleteLogoForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ()

    def save(self, commit=True):
        if self.instance.logo:
            self.instance.logo.delete()
            self.instance.logo_version += 1
            self.instance.logo = generate_logo(self.instance)

        # regenerate a new text-based avatar when profile is deleted.
        self.instance.logo = generate_logo(self.instance)
        return super().save(commit)


class OrganisationsFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["title"].label = ""
        self.fields["communities"].label = ""
        self.fields["services"].label = ""
        self.fields["issues"].label = ""

    class Meta:
        model = OrganisationPage
        fields = ["title", "communities", "services", "issues"]
