from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def replace_with_space(val, replace_from):
	return val.replace(replace_from, " ")