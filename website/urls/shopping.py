from django.conf.urls import url

from website.views.shopping import AddToCartView, RemoveFromCartView, DisplayCartView, ClearCartView, PaymentView, \
    PaymentErrorView, PaymentSuccessView, OrdersView

__author__ = "ckopanos"

urlpatterns = [
    url(r'^add/(?P<software_slug>[\w\s\d_-]+)/(?P<slug>[\w\s\d_-]+)$', AddToCartView.as_view(), {},
        'add-to-cart'),
    url(r'^remove/(?P<cart_item_id>\d+)$', RemoveFromCartView.as_view(), {},
        'remove-from-cart'),
    url(r'^show/$', DisplayCartView.as_view(), {},
        'show-cart'),
    url(r'^clear/$', ClearCartView.as_view(), {},
        'clear-cart'),
    url(r'^your-orders/$', OrdersView.as_view(), {},
        'orders'),
    url(r'^payment/(?P<payment_id>\d+)/$', PaymentView.as_view(), {},
        'checkout-payment'),
    url(r'^payment/failure/(?P<payment_id>\d+)/$', PaymentErrorView.as_view(), {},
        'checkout-payment-error'),
    url(r'^payment/success/(?P<payment_id>\d+)/$', PaymentSuccessView.as_view(), {},
        'checkout-payment-success'),
]