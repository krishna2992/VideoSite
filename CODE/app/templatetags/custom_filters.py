from django import template

register = template.Library()



@register.filter
def captalize_after_hypen(value):
    parts = value.split('-')
    return ' '.join([part.capitalize() for part in parts])

@register.filter
def consolidated_views(value):
    if value >= 1000000:
        return f"{value/1000000:.2f}M"
    elif value>=1000:
        return f"{value/1000:.1f}K"
    else:
        return value