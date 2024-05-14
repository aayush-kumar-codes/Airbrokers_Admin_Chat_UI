# Custom template tags

from django import template
import os

register = template.Library()

@register.filter
def get_filename(url):
    return os.path.basename(url)

@register.filter
def endswith(value, arg):
    """
    Check if the value (URL) ends with the given extension (arg).
    """
    return value.endswith(arg)
