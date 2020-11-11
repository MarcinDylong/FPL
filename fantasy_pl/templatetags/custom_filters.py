from django import template

register = template.Library()

@register.filter(name='give_percent')
def give_percent(value, arg):
    try:
        pr = round((value/arg) * 100, 1)
        return pr
    except:
        return 0


@register.filter(name='give_percent_rev')
def give_percent(value, arg):
    try:
        pr = round(100 - (value/arg) * 100, 1)
        return pr
    except:
        return 0