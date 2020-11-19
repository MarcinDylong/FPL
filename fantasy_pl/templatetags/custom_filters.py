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
def give_percent_rev(value, arg):
    try:
        pr = round(100 - (value/arg) * 100, 1)
        return pr
    except:
        return 0


@register.filter(name='team_role')
def team_role(value, arg):
    if arg == 0:
        value = 'Bench'
        return value
    elif arg == 1:
        value = 'Played'
        return value
    else:
        value = 'Captain'
        return value


@register.filter(name='multiply')
def multiply(value, arg):
    try:
        return arg * value
    except TypeError:
        return 0
