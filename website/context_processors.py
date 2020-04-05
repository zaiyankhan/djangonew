from carton.cart import Cart
from django.conf import settings

__author__ = "ckopanos"

def ui_params(request):
    return {
        'GOOGLE_ANALYTICS_ID': settings.GOOGLE_ANALYTICS_ID
    }

def shopping_cart(request):

    cart = Cart(request.session)
    return {
        'cart': cart
    }