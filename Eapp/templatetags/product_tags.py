from django import template

register=template.Library()
@register.simple_tag
def call_sellprice(price,discount):
    if discount is None or discount is 0:
        return price
    sell=price
    sell=price-(price * discount/100)
    return sell