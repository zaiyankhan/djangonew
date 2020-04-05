import random

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.timezone import now
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

__author__ = "ckopanos"

from decimal import Decimal

from payments import PurchasedItem
from payments.models import BasePayment

class OrderCart(models.Model):
    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    session_key = models.CharField(unique=True, max_length=255)


class OrderItemCart(models.Model):
    class Meta:
        verbose_name = 'Cart item'
        verbose_name_plural = 'Cart items'

    cart = models.ForeignKey(OrderCart, related_name='items', on_delete=models.CASCADE)
    software_pks = models.CharField(max_length=255)
    software = models.ForeignKey('SoftwareProductPricing', on_delete=models.CASCADE)
    modules = models.ManyToManyField('SoftwareModule')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return "%s %s" % (self.software.software.name, self.software.name)

class SoftwareOrder(models.Model):
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.PROTECT)
    order_code = models.CharField(max_length=255)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    company = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True, verbose_name='State / Province')
    country = CountryField(blank=True)
    phone = PhoneNumberField(blank=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return 'Order %s' % self.order_code


class SoftwareOrderItem(models.Model):
    class Meta:
        verbose_name = 'Order item'
        verbose_name_plural = 'Order items'
        ordering = ['-created_at']

    order = models.ForeignKey(SoftwareOrder, related_name='items')
    software = models.ForeignKey('SoftwareProductPricing', null=True, blank=True, on_delete=models.SET_NULL)
    modules = models.ManyToManyField('SoftwareModule', blank=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sku = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Order %s, Item %s" % (self.order.order_code, self.name)


class Payment(BasePayment):

    def get_failure_url(self):
        return reverse('checkout-payment-error', args=[self.pk])

    def get_success_url(self):
        return reverse('checkout-payment-success', args=[self.pk])

    def get_purchased_items(self):
        for item in self.order.items.all():
            yield PurchasedItem(name=item.name, sku=item.sku,
                                quantity=item.quantity,
                                price=item.price, currency=settings.DEFAULT_CURRENCY)

    billing_company = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='payments', null=True, blank=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(SoftwareOrder, related_name='payments')


@receiver(pre_save, sender=SoftwareOrder, dispatch_uid="create_order_code")
def create_order_code(sender, instance, **kwargs):
    if instance.pk is None:
        current_date = now()
        instance.order_code = "%s%s%s%s%s%s-%s" % (instance.user.first_name[:1],
                                                   instance.user.last_name[:1],
                                                   current_date.year,
                                                   current_date.month,
                                                   current_date.day,
                                                   current_date.hour,
                                                   random.randrange(1000, 9999))
