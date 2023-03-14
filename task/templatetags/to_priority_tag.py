from django import template


register = template.Library()


@register.filter
def to_priority_tag(priority):
    if priority == 3:
        return "bg-danger"
    if priority == 2:
        return "bg-primary"
    return "bg-secondary"
