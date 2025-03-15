from django.template import Library
from django.utils.safestring import mark_safe

register = Library()


@register.filter
def verbose_name(obj):
    return obj._meta.verbose_name


def render_list(items):
    html = '<ul>'
    for item in items:
        if isinstance(item, list):
            html += render_list(item)
        else:
            html += f'<li>{item}</li>'
    html += '</ul>'
    return html


@register.filter(is_safe=True)
def html_list(value):
    if not isinstance(value, list):
        return value
    return mark_safe(render_list(value))