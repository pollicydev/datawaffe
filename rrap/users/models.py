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


class User(AbstractUser):
    """
    Default custom user model for rrap.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    first_name = None  # type: ignore
    last_name = None  # type: ignore

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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(_("Your name"), blank=True, max_length=255)
    bio = models.TextField(_("Your bio"), blank=True, max_length=300)

    # avatar stuff
    avatar = models.ImageField(upload_to=get_avatar_full_path, blank=True)
    avatar_version = models.IntegerField(default=0, blank=True, editable=False)

    # The date the user last logged in.
    last_login = models.DateTimeField(null=True, max_length=255, db_index=True)

    # The date the user joined.
    date_joined = models.DateTimeField(auto_now_add=True, max_length=255)
    has_finished_registration = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.get_screen_name()

    def save(self, *args, **kwargs):
        self.date_joined = self.date_joined or timezone.now()
        self.last_login = self.last_login or timezone.now()  # - timedelta(days=1)
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
            if self.user.get_full_name():
                return self.user.get_full_name()
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

    def get_organizations(self):
        Organization = apps.get_model("organizations", "Organization")

        user_organizations = []
        owner_organizations = Organization.objects.select_related(
            "owner__profile"
        ).filter(owner=self.user)
        member_organizations = Organization.objects.select_related(
            "owner__profile"
        ).filter(members=self.user)
        for r in owner_organizations:
            user_organizations.append(r)
        for r in member_organizations:
            user_organizations.append(r)
        user_organizations.sort(key=lambda r: r.last_update, reverse=True)
        return user_organizations

    def get_followers(self):
        Activity = apps.get_model("activities", "Activity")
        activities = Activity.objects.select_related("from_user__profile").filter(
            to_user=self.user, activity_type=ActivityTypes.FOLLOW
        )
        followers = []
        for activity in activities:
            followers.append(activity.from_user)
        return followers

    def get_followers_count(self):
        Activity = apps.get_model("activities", "Activity")
        followers_count = Activity.objects.filter(
            to_user=self.user, activity_type=ActivityTypes.FOLLOW
        ).count()
        return followers_count

    def get_following(self):
        Activity = apps.get_model("activities", "Activity")
        activities = Activity.objects.select_related("to_user__profile").filter(
            from_user=self.user, activity_type=ActivityTypes.FOLLOW
        )
        following = []
        for activity in activities:
            following.append(activity.to_user)
        return following

    def get_following_count(self):
        Activity = apps.get_model("activities", "Activity")
        following_count = Activity.objects.filter(
            from_user=self.user, activity_type=ActivityTypes.FOLLOW
        ).count()
        return following_count
