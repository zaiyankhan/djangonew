from django import forms
from django_countries import countries
from django_countries.fields import CountryField, LazyTypedChoiceField

from website.models import SoftwareOrder

__author__ = "ckopanos"


class SoftwareOrderForm(forms.Form):

    billing_company = forms.CharField(required=False, label='Company')
    billing_first_name = forms.CharField(required=True, label='First name')
    billing_last_name = forms.CharField(required=True, label='Last name')
    billing_address_1 = forms.CharField(required=True, label='Address Line 1')
    billing_address_2 = forms.CharField(required=False, label='Address Line 2')
    billing_city = forms.CharField(required=True, label='City')
    billing_postcode = forms.CharField(required=True, label='Post Code')
    billing_country_code = LazyTypedChoiceField(choices=countries, label='Country')
    billing_country_area = forms.CharField(required=False, label='Area')
    pay_method = forms.CharField(widget=forms.HiddenInput(), required=True)