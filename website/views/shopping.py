from decimal import Decimal

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, mail_managers
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from carton.cart import Cart
from django.template import RequestContext
from django.template.loader import get_template
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, CreateView, FormView, DetailView, ListView, RedirectView
from payments import get_payment_model, RedirectNeeded, PaymentStatus

from website.forms.order import SoftwareOrderForm
from website.models import SoftwareProduct, SoftwareProductPricing, SoftwareOrder, SoftwareOrderItem, Payment, \
    OrderCart, OrderItemCart


class AddToCartView(TemplateView):

    http_method_names = ['post']
    template_name = 'shopping/item_added.html'

    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        cart = Cart(request.session)
        try:
            order_cart = OrderCart.objects.get(session_key=request.session.session_key)
        except OrderCart.DoesNotExist:
            order_cart = OrderCart()
            order_cart.session_key = request.session.session_key
        order_cart.ip_address = request.META.get('REMOTE_ADDRESS', None)
        order_cart.save()
        software = get_object_or_404(SoftwareProduct, slug=kwargs['software_slug'])
        software_modules = request.POST.get('software_modules', None)
        try:
            quantity = int(request.POST.get('quantity', '1'))
        except ValueError:
            quantity = 1
        software_pricing = get_object_or_404(SoftwareProductPricing, software=software, slug=kwargs['slug'], active=True)
        discount = software_pricing.software.additional_license_discount
        price = software_pricing.price
        software_pks = [str(software_pricing.pk)]
        if software_modules:
            software_modules = software_modules.split(",")
            software_modules = software_pricing.active_software_modules.filter(pk__in=software_modules)
            for software_module in software_modules:
                software_pks.append("m_%s" % software_module.pk)
                price += software_module.price
        try:
            order_cart_item = OrderItemCart.objects.get(cart=order_cart, software_pks=",".join(software_pks))
            order_cart_item.price = price
            order_cart_item.quantity = order_cart_item.quantity + quantity
            quantity = order_cart_item.quantity
        except OrderItemCart.DoesNotExist:
            order_cart_item = OrderItemCart()
            order_cart_item.cart = order_cart
            order_cart_item.software_pks = ",".join(software_pks)
            order_cart_item.software = software_pricing
            order_cart_item.price = price
            order_cart_item.quantity = quantity
            order_cart_item.save()
            if software_modules:
                order_cart_item.modules = software_modules
        if discount > 0 and quantity > 1:
            additional_license_price = price - (price * discount / 100)
            additional_licenses_price = additional_license_price * (quantity - 1)
            price = (price + additional_licenses_price) / quantity
            order_cart_item.price = price
        order_cart_item.save()
        cart.remove(order_cart_item)
        cart.add(order_cart_item, price=order_cart_item.price, quantity=quantity)
        context = self.get_context_data(**kwargs)
        context.update({
            'software': software,
            'order_cart_item': order_cart_item
        })
        return self.render_to_response(context)


class RemoveFromCartView(TemplateView):

    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        cart = Cart(request.session)
        try:
            cart_item = OrderItemCart.objects.get(pk=kwargs['cart_item_id'], cart__session_key=request.session.session_key)
        except OrderItemCart.DoesNotExist:
            return HttpResponseRedirect(reverse('show-cart'))
        cart.remove(cart_item)
        cart_item.delete()
        return HttpResponseRedirect(reverse('show-cart'))


class ClearCartView(TemplateView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        cart = Cart(request.session)
        cart.clear()
        try:
            order_cart = OrderCart.objects.get(session_key=request.session.session_key)
            order_cart.delete()
        except OrderCart.DoesNotExist:
            pass
        return JsonResponse({'cleared': True})


@method_decorator(login_required, name='post')
class DisplayCartView(FormView):

    template_name = 'shopping/cart.html'
    form_class = SoftwareOrderForm

    def get_initial(self):
        initial = super().get_initial()
        billing_details = None
        if 'billing_details' in self.request.session:
            billing_details = self.request.session['billing_details']
        else:
            #try to find a last payment made by the user
            if self.request.user.is_authenticated:
                a_payment = Payment.objects.filter(user=self.request.user).order_by('-created')[:1]
                if a_payment:
                    recent_paymnent = a_payment[0]
                    billing_details = {
                        'billing_first_name': recent_paymnent.billing_first_name,
                        'billing_last_name': recent_paymnent.billing_last_name,
                        'billing_company': recent_paymnent.billing_company,
                        'billing_country_code': recent_paymnent.billing_country_code,
                        'billing_city': recent_paymnent.billing_city,
                        'billing_country_area': recent_paymnent.billing_country_area,
                        'billing_address_1': recent_paymnent.billing_address_1,
                        'billing_address_2': recent_paymnent.billing_address_2,
                        'billing_postcode': recent_paymnent.billing_postcode
                    }
                    self.request.session['billing_details'] = billing_details
        if self.request.user.is_authenticated:
            initial.update({
                'billing_first_name': billing_details['billing_first_name'] if billing_details else self.request.user.first_name,
                'billing_last_name': billing_details['billing_last_name'] if billing_details else self.request.user.last_name,
                'billing_company': billing_details['billing_company'] if billing_details else self.request.user.company,
                'billing_country_code': billing_details['billing_country_code'] if billing_details else self.request.user.country,
                'billing_city': billing_details['billing_city'] if billing_details else self.request.user.city,
                'billing_country_area': billing_details['billing_country_area'] if billing_details else self.request.user.state,
                'billing_address_1': billing_details['billing_address_1'] if billing_details else "",
                'billing_address_2': billing_details['billing_address_2'] if billing_details else "",
                'billing_postcode': billing_details['billing_postcode'] if billing_details else ""
            })
        return initial

    def form_valid(self, form):
        form_data = form.cleaned_data
        if 'order_in_session' in self.request.session:
            try:
                order = SoftwareOrder.objects.get(pk=self.request.session['order_in_session'])
            except SoftwareOrder.DoesNotExist:
                order = SoftwareOrder()
        else:
            order = SoftwareOrder()
        cart = Cart(self.request.session)
        order.total = cart.total
        order.user = self.request.user
        order.company = self.request.user.company
        order.first_name = self.request.user.first_name
        order.last_name = self.request.user.last_name
        order.email = self.request.user.email
        order.city = self.request.user.city
        order.state = self.request.user.state
        order.country = self.request.user.country
        order.phone = self.request.user.phone
        order.is_completed = False
        order.save()
        self.request.session['order_in_session'] = order.pk
        order.items.all().delete()
        for item in cart.items:
            order_item = SoftwareOrderItem()
            order_item.software = item.product.software
            order_item.quantity = item.quantity
            order_item.price = item.price
            order_item.name = "%s" % item.product
            order_item.sku = item.product.software.sku
            order_item.order = order
            order_item.save()
            if item.product.modules.exists():
                order_item.modules = item.product.modules.all()
                module_names = []
                module_skus = []
                for module in order_item.modules.all():
                    module_names.append(module.name)
                    module_skus.append(module.sku)
                order_item.name = "%s Plus %s" % (order_item.name, ", ".join(module_names))
                order_item.sku = "%s %s" % (order_item.sku, " ".join(module_skus))
                order_item.save()
        self.request.session['billing_details'] = {
            'billing_first_name': form_data['billing_first_name'],
            'billing_last_name': form_data['billing_last_name'],
            'billing_company': form_data['billing_company'],
            'billing_country_code': form_data['billing_country_code'],
            'billing_city': form_data['billing_city'],
            'billing_country_area': form_data['billing_country_area'],
            'billing_address_1': form_data['billing_address_1'],
            'billing_address_2': form_data['billing_address_2'],
            'billing_postcode': form_data['billing_postcode']
        }
        Payment = get_payment_model()
        payment = Payment.objects.create(
            variant=form_data['pay_method'],  # this is the variant from PAYMENT_VARIANTS
            description=order.order_code,
            order=order,
            user=self.request.user,
            total=cart.total,
            tax=Decimal(0),
            currency=settings.DEFAULT_CURRENCY,
            delivery=Decimal(0),
            billing_first_name=form_data['billing_first_name'],
            billing_last_name=form_data['billing_last_name'],
            billing_company=form_data['billing_company'],
            billing_address_1=form_data['billing_address_1'],
            billing_address_2=form_data['billing_address_2'],
            billing_city=form_data['billing_city'],
            billing_postcode=form_data['billing_postcode'],
            billing_country_code=form_data['billing_country_code'],
            billing_country_area=form_data['billing_country_area'],
            customer_ip_address=self.request.META.get('REMOTE_ADDR'))
        return redirect(reverse('checkout-payment', args=[payment.pk]))


@method_decorator(login_required, name='dispatch')
class PaymentView(DetailView):

    pk_url_kwarg = 'payment_id'
    model = Payment
    template_name = 'shopping/payment.html'
    context_object_name = 'payment'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            form = self.object.get_form()
        except RedirectNeeded as redirect_to:
            return redirect(str(redirect_to))
        context = self.get_context_data(object=self.object)
        context.update({
            'form': form
        })
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            form = self.object.get_form(data=request.POST)
        except RedirectNeeded as redirect_to:
            return redirect(str(redirect_to))
        context = self.get_context_data(object=self.object)
        context.update({
            'form': form
        })
        return self.render_to_response(context)




class PaymentErrorView(TemplateView):

    template_name = "shopping/payment_error.html"


@method_decorator(login_required, name='dispatch')
class PaymentSuccessView(TemplateView):
    template_name = "shopping/payment_error.html"

    def get(self, request, *args, **kwargs):
        try:
            payment = Payment.objects.get(pk=kwargs['payment_id'], user=self.request.user)
        except Payment.DoesNotExist:
            raise Http404
        if payment.status == PaymentStatus.PREAUTH:
            try:
                payment.capture()
            except Exception as e:
                pass
        if payment.status != PaymentStatus.CONFIRMED:
            return redirect(reverse('checkout-payment-error', args=[payment.pk]))
        order = payment.order
        order.is_completed = True
        order.save()
        cart = Cart(self.request.session)
        cart.clear()
        try:
            order_cart = OrderCart.objects.get(session_key=request.session.session_key)
            order_cart.delete()
        except OrderCart.DoesNotExist:
            pass
        currentSite = get_current_site(request)
        subject = 'About your order at %(site)s' % {'site': currentSite.name}
        html = get_template('email/shopping/new_order.html')
        txt = get_template('email/shopping/new_order.txt')
        d = RequestContext(request, {"full_name": request.user.full_name, "order": order,
                                     "domain": currentSite.domain, "protocol": request.scheme})
        html = html.render(d)
        plaintext = txt.render(d)
        send_mail(subject, plaintext, settings.GENERIC_EMAIL_FROM, [request.user.email], fail_silently=True, html_message=html)
        mail_managers("New order at %s" % currentSite.name, "A new order with code %s has been placed. "
                                                            "Please access "
                                                            "the backend to check the order details" % order.order_code,
                      fail_silently=False, html_message=html)
        del request.session['order_in_session']
        return redirect(reverse('orders'))
        return super().get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class OrdersView(ListView):

    template_name = "account/orders.html"

    def get_queryset(self):
        return SoftwareOrder.objects.filter(user=self.request.user, is_completed=True)