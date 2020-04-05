from django.db.models.signals import post_save
from django.utils import timezone

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail, mail_managers
from django.db import models
from django.utils.functional import cached_property
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

class Account(models.Model):

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True)
    country = CountryField(null=True, blank=True)
    phone = PhoneNumberField(blank=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

class BusinessType(models.Model):

    class Meta:
        verbose_name = 'Business Type'
        verbose_name_plural = 'Business Types'

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ClientInterests(models.Model):

    class Meta:
        verbose_name_plural = 'Clients Interests'
        verbose_name = 'Client interest'

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class AppUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=AppUserManager.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
                                password=password,
                                first_name=first_name,
                                last_name=last_name
                                )
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class AppUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']


    email = models.EmailField(
        verbose_name=_('Email'),
        max_length=255,
        unique=True,
        db_index=True,
    )
    first_name = models.CharField(max_length=255, verbose_name=_("First name"))
    last_name = models.CharField(max_length=255, verbose_name=_("Last name"))
    is_active = models.BooleanField(default=False, verbose_name=_("Is active"))
    is_staff = models.BooleanField(default=False, verbose_name=_("Is staff"))
    date_joined = models.DateTimeField(default=timezone.now, verbose_name=_("Date joined"))
    company = models.CharField(max_length=255, null=True, blank=True)
    business_type = models.ForeignKey(BusinessType, related_name='clients', null=True, blank=True, on_delete=models.PROTECT)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True, verbose_name='State / Province')
    country = CountryField(blank=True)
    phone = PhoneNumberField(blank=True, help_text='e.g. +41524204242')
    receive_newsletter = models.BooleanField(default=True)
    interested_in = models.ManyToManyField(ClientInterests, related_name='clients')
    synced_with_mailchimp = models.BooleanField(default=False)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True)
    is_account_admin = models.BooleanField(default=False)
    objects = AppUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        # The user is identified by their full name
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def __str__(self):
        return self.get_full_name()

    @property
    def full_name(self):
        return self.get_full_name()

    @property
    def username(self):
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @cached_property
    def interested(self):
        interests = []
        for interest in self.interested_in.all():
            interests.append(interest.name)
        return ", ".join(interests)

    @property
    def email_address_details(self):
        return "Telephone:%s\nCompany: %s\nAddress: %s, %s %s" % (self.phone, self.company, self.city, self.state, self.country)