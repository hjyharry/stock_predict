from django import template

register = template.Library()

@register.filter(name='percent')
def percent(value):
    if value == '':
        value = 0
        return round(float(value) * 100, 2)
    else:
        return round(float(value) * 100, 2)

@register.filter(name='thousands')
def thousands(value):
    if value == '':
        value = 0
        return round(float(value) / 1000000, 2)
    else:
        return round(float(value) / 1000000, 2)


@register.filter(name='million')
def million(value):
    if value == '':
        value = 0
        return round(float(value) / 10000, 2)
    else:
        return round(float(value) / 10000, 2)

@register.filter(name="billion")
def billion(value):
    if value == '':
        value = 0
        return round(float(value) / 100000000, 2)
    else:
        return round(float(value) / 100000000, 2)
