from django import template

register = template.Library()


@register.filter(name='addCss')
def addCss(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter(name='get_fields')
def get_fields(obj):
    return [(field.name, field.value_to_string(obj)) for field in obj._meta.fields]
