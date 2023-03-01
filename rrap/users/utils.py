from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import User, generate_avatar, Profile
from django.conf import settings
import hashlib
import urllib.parse as urlparse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class ProfileForm(forms.ModelForm):
    bio = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control expanding", "rows": "3"}),
        max_length=500,
        required=False,
    )

    class Meta:
        model = Profile
        fields = (
            "name",
            "bio",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control form-control-lg"
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "name",
            "bio",
            Submit("submit", "Update profile"),
        )

        self.fields["name"].label = ""
        self.fields["bio"].label = ""


class OnboardingForm(forms.ModelForm):
    bio = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control expanding", "rows": "3"}),
        max_length=500,
        required=False,
    )

    class Meta:
        model = Profile
        fields = (
            "name",
            "bio",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "name",
            "bio",
            Submit("submit", "Update profile"),
        )


class PasswordProtectedForm(forms.Form):
    password = forms.CharField(
        strip=False,
        label="",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter your password and hit ENTER",
                "class": "form-control form-control-lg",
            },
        ),
    )

    def clean_password(self):
        """Validate that the entered password is correct."""
        password = self.cleaned_data["password"]
        if not self.user.check_password(password):
            raise forms.ValidationError(
                _("The password is incorrect"), code="password_incorrect"
            )
        return password


class DeleteAvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ()

    def save(self, commit=True):
        if self.instance.avatar:
            self.instance.avatar.delete()
            self.instance.avatar_version += 1
            self.instance.avatar = generate_avatar(self.instance)

        # regenerate a new text-based avatar when profile is deleted.
        self.instance.avatar = generate_avatar(self.instance)
        return super().save(commit)


def gravatar_url(email, style="mp", size=80):
    hash_num = hashlib.md5(email).hexdigest()

    url = "https://secure.gravatar.com/avatar/%s?" % hash_num
    url += urlparse.urlencode(
        {
            "s": str(size),
            "d": style,
        }
    )
    return url


def gravatar(user, size=80):
    if not user or user.is_anonymous:
        email = "anon@datawaffe.org".encode("utf8")
        return gravatar_url(email=email)

    email = user.email if user.is_authenticated else ""
    email = email.encode("utf8")

    style = settings.GRAVATAR_ICON or "retro"

    return gravatar_url(email=email, style=style, size=size)
