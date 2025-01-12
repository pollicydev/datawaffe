from django.contrib.auth.models import AbstractUser
from django.apps import apps
import pyavagen
import io
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.files.base import ContentFile
from django.utils import timezone
from rrap.activities.constants import ActivityTypes
from django_countries.fields import CountryField
from django_fsm import FSMField, transition


class User(AbstractUser):
    """
    Default custom user model for rrap.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    first_name = models.CharField(max_length=150, blank=True, verbose_name="first name")
    last_name = models.CharField(max_length=150, blank=True, verbose_name="last name")

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


def get_avatar_full_path(instance, filename):
    ext = filename.split(".")[-1]
    path = f"{settings.MEDIA_PUBLIC_ROOT}/avatars"
    name = f"{instance.id}_{instance.avatar_version:04d}"
    return f"{path}/{name}.{ext}"


def generate_avatar(user):
    img_io = io.BytesIO()
    avatar = pyavagen.Avatar(
        pyavagen.CHAR_SQUARE_AVATAR, size=500, string=user.name, blur_radius=100
    )
    avatar.generate().save(img_io, format="PNG", quality=100)
    img_content = ContentFile(img_io.getvalue(), f"{user.pk}.png")

    return img_content


def change_avatar(user, image_file):
    if user.avatar:
        user.avatar.delete()
    user.avatar_version += 1
    user.avatar = image_file
    user.save()

    return user


class Profile(models.Model):

    NO = 0
    YES = 1
    BOOLEAN_CHOICES = ((NO, "No"), (YES, "Yes"))

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    REVIEW_CHOICES = (
        (PENDING, "Pending Review"),
        (APPROVED, "Approved"),
        (REJECTED, "Rejected"),
    )

    # Pronouns
    NONE = 0
    HE = 1
    SHE = 2
    THEY = 3
    ZE = 4
    XE = 5
    SHE_THEY = 6
    HE_THEY = 7
    OTHER = 8

    PRONOUNS = (
        (NONE, "Just my name please!"),
        (HE, "he/him/his"),
        (SHE, "She/her/hers"),
        (THEY, "They/them/theirs"),
        (ZE, "Ze/hir/hirs"),
        (XE, "Xe/xem/xyr"),
        (SHE_THEY, "She/they"),
        (HE_THEY, "he/they"),
        (OTHER, "Other"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(_("Your full name"), blank=True, max_length=255)
    pronouns = models.SmallIntegerField(
        "What are your pronouns?",
        choices=PRONOUNS,
        default=0,
    )
    other_pronouns = models.CharField(
        "Other pronouns",
        max_length=255,
        help_text="Please specify your pronouns if missing",
        blank=True,
        null=True,
    )
    country = CountryField(blank_label="Select country", blank=True)
    why = models.TextField(
        _("Why are you here?"),
        blank=True,
        max_length=500,
    )

    # avatar stuff
    avatar = models.ImageField(upload_to=get_avatar_full_path, blank=True)
    avatar_version = models.IntegerField(default=0, blank=True, editable=False)

    # The date the user joined.
    date_joined = models.DateTimeField(auto_now_add=True, max_length=255)
    has_finished_registration = models.BooleanField(default=False, null=True)
    review_status = models.CharField(
        "Review status", max_length=10, choices=REVIEW_CHOICES, default="pending"
    )
    is_ukpc_affiliate = models.SmallIntegerField(
        "Is the organisation you are affiliated too a member of UKPC?",
        choices=BOOLEAN_CHOICES,
        default=1,
    )
    organisation = models.ForeignKey(
        "organizations.OrganisationPage",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Select UKPC organisation"),
    )
    custom_affiliation = models.CharField(
        _("Affiliation"), blank=True, max_length=255, null=True
    )
    is_datauser = models.SmallIntegerField(
        choices=BOOLEAN_CHOICES,
        default=0,
    )

    def __str__(self):
        return self.get_screen_name()

    def save(self, *args, **kwargs):
        self.date_joined = self.date_joined or timezone.now()
        super(Profile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    def get_initials(self):
        xs = self.name
        name_list = xs.split()
        initials = ""

        for name in name_list:  # go through each name
            initials += name[0].upper()  # append the initial

        return initials

    def get_screen_name(self):
        try:
            if not self.user.get_full_name() == "None None":
                return self.user.get_full_name()

            elif self.name:
                return self.name
            else:
                return self.user.username
        except Exception:
            return self.user.username

    def recently_joined(self):
        """
        User that joined X amount of days are considered new.
        """
        recent = (
            timezone.now() - self.date_joined
        ).days > settings.RECENTLY_JOINED_DAYS
        return recent

    def get_following(self):
        Activity = apps.get_model("activities", "Activity")
        activities = Activity.objects.select_related("organisation").filter(
            from_user=self.user, activity_type=ActivityTypes.FOLLOW
        )
        following = []
        for activity in activities:
            following.append(activity.organisation)
        return following

    def get_following_count(self):
        Activity = apps.get_model("activities", "Activity")
        following_count = Activity.objects.filter(
            from_user=self.user, activity_type=ActivityTypes.FOLLOW
        ).count()
        return following_count

    def state_color(self):
        if self.review_status == "pending":
            return "#ffa500"
        elif self.review_status == "approved":
            return "#189370"
        elif self.review_status == "rejected":
            return "#cd3238"
        else:
            return "#000"

    class Meta:
        verbose_name = "Data User"
        verbose_name_plural = "Data Users"
