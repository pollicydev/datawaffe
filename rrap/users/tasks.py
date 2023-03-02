from django.conf import settings
from django.conf import settings
from django.core.mail import send_mail


def send_welcome_email(user):

    from_email = settings.DEFAULT_FROM_EMAIL
    template = "account/email/welcome.txt"
    email_list = [user.email]
    context = dict(user=user, name=user.get_screen_name)
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
    send_welcome_email(user=user)
    return
