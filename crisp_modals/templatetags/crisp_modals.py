from django.template import Library

register = Library()


@register.filter
def verbose_name(obj):
    return obj._meta.verbose_name

