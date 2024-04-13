# Custom template tags

from django import template
import os

register = template.Library()

@register.filter
def get_filename(url):
    return os.path.basename(url)
