from datetime import date
from django import template
from r2e.commom import short_name

register = template.Library()


@register.filter(name="age")
def age(birth):
    return (date.today() - birth).days // 365


@register.filter(name="shortname")
def shortname(name):
    return short_name(name)


@register.filter(name="has_group")
def has_group(user, group_names):
    if user.is_superuser:
        return True
    groups = user.groups.values_list("name", flat=True)
    return any(group in groups for group in group_names.split(","))
