from django.contrib.auth.mixins import UserPassesTestMixin


class ProfileOwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.kwargs["username"] == self.request.user.username


class UserActiveMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_active == True
