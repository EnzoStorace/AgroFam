from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiplica o valor por outro argumento (quantidade)."""
    try:
        return value * arg
    except (ValueError, TypeError):
        return value
