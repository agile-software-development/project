from django import template


register = template.Library()


@register.filter
def in_state(tasks, state):
    return tasks.filter(state=state)
