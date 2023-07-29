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


@register.filter(name="in_group")
def in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
