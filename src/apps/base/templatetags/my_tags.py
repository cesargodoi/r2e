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
