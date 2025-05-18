from django import template

register = template.Library()

@register.filter(name='currency')
def currency(number):
    return f"BDT {number}"

@register.filter(name='multiply')
def multiply(number, multiplier):
    return number * multiplier
