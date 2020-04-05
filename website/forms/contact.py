from phonenumber_field.formfields import PhoneNumberField

__author__ = 'ckopanos'


from django import forms


class ContactForm(forms.Form):

    message = forms.CharField(required=True, widget=forms.Textarea, label='Your request')
    name = forms.CharField(required=True, label='Fullname')
    email = forms.EmailField(required=True, label='Email address')
    phone = PhoneNumberField(required=True, label='Telephone')