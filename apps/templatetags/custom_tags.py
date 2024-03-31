from django.template import Library

from apps.models import Wishlist

register = Library()


@register.filter()
def custom_slice(value, arg):
    a, b = map(int, arg.split(':'))
    return list(value)[a:b]


@register.filter()
def has_wishlist(user_id, product_id):
    return Wishlist.objects.filter(user_id=user_id, product_id=product_id).exists()
