from datetime import date
from django import template

register = template.Library()


@register.filter(name="age")
def age(birth):
    return (date.today() - birth).days // 365
