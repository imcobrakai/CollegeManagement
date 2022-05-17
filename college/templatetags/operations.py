from atexit import register
from django import template

register = template.Library()

@register.filter
def divide(value, args):
    if float(args) == 0:
        return f"0%"
    return "{:.2f}%".format((float(value) / float(args) * 100))
