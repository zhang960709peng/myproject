from django.template import Library

register = Library()

@register.filter
def myslice(value):
    if len(value)>10:
        value = value[:10]+"..."
    return value


@register.filter
def myslice2(value,num):
    if len(value)>num:
        value = value[:num]+"..."
    return value

@register.filter
def mysum(value,nums):
    return sum([int(i) for i in nums.split(",")])+value