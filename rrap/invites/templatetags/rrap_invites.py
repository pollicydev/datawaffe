from django import template
from django.utils.html import format_html

from ..constants import InviteStatus

register = template.Library()


@register.simple_tag()
def invite_status(invite):
    css_classes = {
        InviteStatus.PENDING: "badge-warning",
        InviteStatus.ACCEPTED: "badge-success",
        InviteStatus.REJECTED: "badge-danger",
    }
    return format_html(
        "<span class='badge {css_class}'>{label}</span>",
        css_class=css_classes.get(invite.status),
        label=invite.get_status_display(),
    )
