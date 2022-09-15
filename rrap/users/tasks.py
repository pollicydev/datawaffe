from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail


account_verification_token = PasswordResetTokenGenerator()

def send_verification_email(user):

    from_email = settings.DEFAULT_FROM_EMAIL
    userid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_verification_token.make_token(user)
    template = "accounts/email_verify.html"
    email_list = [user.email]
    context = dict(token=token, userid=userid, user=user)
    subject = "Welcome Aboard!"
    # Send the verification email
    send_mail(
        html_message=template,
        recipient_list=email_list,
        extra_context=context,
        from_email=from_email,
        subject=subject,
    )

    return True


def message(msg, level=0):
    print(f"{msg}")

def verification_email(user):
    send_verification_email(user=user)
    return