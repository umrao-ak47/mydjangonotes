from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.filter(name='markup')
def markup_text(text: str) -> str:
    return mark_safe(markdown.markdown(text))