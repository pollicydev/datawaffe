from django.conf import settings
from django.shortcuts import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string


def send_welcome_email(user):

    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [
        user.email,
    ]
    context = {
        "user": user,
        "name": user.profile.get_screen_name(),
        "contact_link": "https://datawaffe.org/contact",
        "terms_link": "https://datawaffe.org/terms-and-conditions",
    }
    subject = "Account Approval and Terms Reminder"
    message = render_to_string("account/email/welcome.txt", context)
    try:
        send_mail(subject, message, from_email, recipient_list)
    except BadHeaderError:
        return HttpResponse("Invalid header found.")

    return True


def send_delay_notice(user):

    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [
        user.email,
    ]
    context = {
        "user": user,
        "name": user.profile.get_screen_name(),
        "contact_link": "https://datawaffe.org/contact",
    }
    subject = "Data Waffe Account Creation - Approval Delay Notice"
    message = render_to_string("account/email/delay_notice.txt", context)
    try:
        send_mail(subject, message, from_email, recipient_list)
    except BadHeaderError:
        return HttpResponse("Invalid header found.")

    return True


def send_rejection_notice(user):

    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [
        user.email,
    ]
    context = {
        "user": user,
        "name": user.profile.get_screen_name(),
        "contact_link": "https://datawaffe.org/contact",
    }
    subject = "Data Waffe Account Creation - Rejection Notice"
    message = render_to_string("account/email/rejection_notice.txt", context)
    try:
        send_mail(subject, message, from_email, recipient_list)
    except BadHeaderError:
        return HttpResponse("Invalid header found.")

    return True


def message(msg, level=0):
    print(f"{msg}")


def welcome_email(user):
    send_welcome_email(user=user)
    return
