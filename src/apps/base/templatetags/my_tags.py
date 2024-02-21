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


@register.filter(name="has_user")
def has_user(user):
    groups = user.groups.values_list("name", flat=True)
    return "user" in groups


@register.filter(name="has_group")
def has_group(user, group_names):
    if user.is_superuser:
        return True
    groups = user.groups.values_list("name", flat=True)
    return any(group in groups for group in group_names.split(","))


@register.filter(name="same_center")
def same_center(user, center_id):
    if user.is_superuser:
        return True
    return user.person.center_id == center_id


@register.filter(name="delete_permission")
def delete_permission(user, link):
    if user.is_superuser:
        return True
    groups = user.groups.values_list("name", flat=True)
    app = link.split("/")[1]
    return "admin" in groups and app not in ["event"]


@register.filter(name="get_item")
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter(name="get_abs")
def get_abs(num):
    return abs(num)
