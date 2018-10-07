from django import template

register = template.Library()


@register.inclusion_tag("commons/templatetags/actions.html")
def actions(object, edit, remove):
    return {'object': object, 'edit': edit, 'remove': remove}
