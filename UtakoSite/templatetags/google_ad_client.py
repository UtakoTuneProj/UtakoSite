from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def google_ad_client():
    return settings.GOOGLE_AD_CLIENT
