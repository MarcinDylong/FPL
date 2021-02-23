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
        return 'Bench'
    elif arg == 1:
        return 'Played'
    elif arg == 2:
        return 'Captain'
    else:
        return 'T. Captain'


@register.filter(name='multiply')
def multiply(value, arg):
    try:
        return arg * value
    except TypeError:
        return 0


@register.filter(name='division')
def division(value, arg):
    try:
        return round(value/arg,2 )
    except (TypeError, ZeroDivisionError):
        return 0
