# -*- coding: utf-8 -*-
import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm, ReadOnlyPasswordHashField
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from website.models import AppUser
from website.models import ClientInterests

__author__ = 'ckopanos'


class PasswordResetForm(PasswordResetForm):
    pass


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'duplicate_email': _('This is email address already exists'),
        'password_mismatch': _('The two passwords do not match'),
        'wrong_first_name': _('Your first name must contain characters only'),
        'wrong_last_name': _('Your last name must contain characters only')
    }
    email = forms.EmailField()
    password1 = forms.CharField(label=_('Password'),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password again'),
                                widget=forms.PasswordInput,
                                help_text=_('Fill in your password again for verification'))

    class Meta:
        model = AppUser
        fields = ("email", "first_name", "last_name")

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            AppUser._default_manager.get(email=email)
        except AppUser.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])

    def clean_first_name(self):
        name = self.cleaned_data.get('first_name')
        if re.search('[\.\-\$\#\&\^\@\!\%\*\(\)0-9\+\-]+', name, re.UNICODE):
            raise forms.ValidationError(self.error_messages['wrong_first_name'])
        return name

    def clean_last_name(self):
        name = self.cleaned_data.get('last_name')
        if re.search('[\.\-\$\#\&\^\@\!\%\*\(\)0-9\+\-]+', name, re.UNICODE):
            raise forms.ValidationError(self.error_messages['wrong_last_name'])
        return name

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    MIN_LENGTH = 6

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        # At least MIN_LENGTH long
        if len(password1) < self.MIN_LENGTH:
            raise forms.ValidationError(_("Your password should contain at least %d χαρακτήρες." % self.MIN_LENGTH))

        return password1

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    error_messages = {
        'duplicate_email': _('There is email address already exists'),
        'password_mismatch': _('The two passwords do not match'),
        'wrong_first_name': _('Your first name must contain characters only'),
        'wrong_last_name': _('Your last name must contain characters only')
    }

    class Meta:
        model = AppUser
        fields = ['first_name', 'last_name', 'company', 'business_type', 'city', 'state', 'country',
                  'phone', 'receive_newsletter', 'interested_in']

    def clean_email(self):
        email = self.cleaned_data["email"]
        users = AppUser.objects.filter(email=email).exclude(pk=self.instance.pk).all()
        if not users:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])

    def clean_first_name(self):
        name = self.cleaned_data.get('first_name')
        if re.search('[\.\-\$\#\&\^\@\!\%\*\(\)0-9\+\-]+', name, re.UNICODE):
            raise forms.ValidationError(self.error_messages['wrong_first_name'])
        return name

    def clean_last_name(self):
        name = self.cleaned_data.get('last_name')
        if re.search('[\.\-\$\#\&\^\@\!\%\*\(\)0-9\+\-]+', name, re.UNICODE):
            raise forms.ValidationError(self.error_messages['wrong_last_name'])
        return name


class UserChangeFormAdmin(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ("email", "first_name", "last_name")

    password = ReadOnlyPasswordHashField(label=_("Password"),
                                         help_text=_("Raw passwords are not stored, so there is no way to see "
                                                     "this user's password, but you can change the password "
                                                     "using <a href=\"../password/\">this form</a>."))

    def clean_email(self):
        email = self.cleaned_data["email"]
        users = AppUser.objects.filter(email=email).exclude(pk=self.instance.pk).all()
        if not users:
            return email
        raise forms.ValidationError(_("A user with that email address already exists."))

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ("first_name", "last_name", 'company', 'business_type',
                  'interested_in', 'city', 'state', 'country', 'phone', 'receive_newsletter')
        widgets = {
            'country': CountrySelectWidget(attrs={'class': 'selectize'})
        }

    interested_in = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'selectize'}),
                                                   queryset=ClientInterests.objects.all())
    phone = PhoneNumberField(label='Phone', widget=PhoneNumberPrefixWidget(attrs={
                                                                                  'class': 'form-control'}))

    def signup(self, request, user):
        form_data = self.cleaned_data
        user.first_name = form_data['first_name']
        user.last_name = form_data['last_name']
        user.company = form_data['company']
        user.business_type = form_data['business_type']
        user.interested_in = form_data['interested_in']
        user.city = form_data['city']
        user.state = form_data['state']
        user.country = form_data['country']
        user.phone = form_data['phone']
        user.receive_newsletter = form_data['receive_newsletter']
        user.is_active = True
        user.save()

