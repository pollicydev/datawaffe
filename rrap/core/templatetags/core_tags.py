import random
from django import template
from rrap.core.models import KeyPopulation, Violation

register = template.Library()


@register.simple_tag
def get_community_name(community_id):
    community = None
    try:
        community = KeyPopulation.objects.get(id=community_id)
        return community.title
    except:
        KeyPopulation.DoesNotExist


@register.simple_tag
def get_community_acronym(community_id):
    community = None
    try:
        community = KeyPopulation.objects.get(id=community_id)
        return community.acronym
    except:
        KeyPopulation.DoesNotExist


@register.simple_tag
def get_community_color(community_id):
    community = None
    try:
        community = KeyPopulation.objects.get(id=community_id)
        return community.color
    except:
        KeyPopulation.DoesNotExist


@register.simple_tag
def get_community_color_in_rgb(community_id):
    hexcode = (KeyPopulation.objects.get(id=community_id).color).lstrip("#")
    rgb = tuple(int(hexcode[i : i + 2], 16) for i in (0, 2, 4))
    return rgb


@register.simple_tag
def hex_to_rgb(hexcode):
    stripped = hexcode.lstrip("#")
    return tuple(int(stripped[i : i + 2], 16) for i in (0, 2, 4))


@register.simple_tag
def get_violation(violation_id):
    violation = None
    try:
        violation = Violation.objects.get(id=violation_id)
        return violation.title
    except:
        Violation.DoesNotExist


@register.simple_tag
def generate_violation_hex(violation_id):
    violation = None
    try:
        violation = Violation.objects.get(id=violation_id)
        return violation.color
    except:
        Violation.DoesNotExist
