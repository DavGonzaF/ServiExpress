from django import template

register = template.Library()

@register.filter
def map(attribute, items):
    return [getattr(item, attribute) for item in items]

@register.filter
def sum(items):
    return sum(items)


@register.filter
def sum_subtotals(items):
    return sum(item['subtotal'] for item in items)
    
register = template.Library()

@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})

@register.filter
def multiply(value, arg):
    """Multiplica dos valores."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0