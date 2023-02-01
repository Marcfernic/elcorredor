from django import template
from django.urls import reverse

register = template.Library()

@register.filter(name = 'active_class_for')
def active_class_for(request, url_name):
    if request.path == reverse(url_name):
        return "active"
    else:
        return ""
