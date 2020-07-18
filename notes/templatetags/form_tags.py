from django import template
from django.forms import BoundField

register = template.Library()

@register.filter(name='class_attr')
def class_attr(text: BoundField, args: str) -> BoundField:
    css_cls = ' '.join([c.strip() for c in args.split(',')])
    return text.as_widget(attrs={'class':'{}'.format(css_cls)})