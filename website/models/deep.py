from autoslug import AutoSlugField
from cms.models import PlaceholderField, reverse, Site
from django.db import models
from django.db.models import FileField
from django.utils.functional import cached_property
from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField
import os

__author__ = "ckopanos"


class SoftwareProduct(models.Model):
    class Meta:
        verbose_name = 'Software product'
        verbose_name_plural = 'Software products'

    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)
    short_description = HTMLField(null=True, blank=True)
    meta_title = models.CharField(max_length=70)
    meta_description = models.CharField(max_length=160)
    description = PlaceholderField('software_description', related_name='software_product_descriptions')
    description = PlaceholderField('software_sidebar', related_name='software_product_sidebars')
    logo = FilerImageField(null=True, blank=True, related_name="software_logos")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    demo = FileField(null=True, blank=True, upload_to='downloads')
    read_more_link = models.CharField(null=True, blank=True, max_length=255)
    active = models.BooleanField(default=True)
    additional_license_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sites = models.ManyToManyField(Site)

    def __str__(self):
        return self.name

    @cached_property
    def active_pricing(self):
        return self.pricing.filter(active=True).select_related('software')

    @cached_property
    def starting_at_price(self):
        price = self.active_pricing.filter(is_service=False).order_by('price')[:1]
        if price:
            return price[0]
        return None

    @cached_property
    def file_type(self):
        elements = os.path.splitext(os.path.basename(self.demo.path))
        if len(elements) == 2:
            return elements[1]
        return '.exe'

    def download_url(self):
        return reverse('download-software', kwargs={'slug': self.slug})


class SoftwareModule(models.Model):
    class Meta:
        verbose_name = 'Software module'
        verbose_name_plural = 'Software modules'

    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)
    software = models.ForeignKey(SoftwareProduct, related_name='modules')
    sku = models.CharField(max_length=255, unique=True)
    short_description = HTMLField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    read_more_link = models.CharField(null=True, blank=True, max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "%s %s" % (self.software.name, self.name)

class SoftwareProductPricing(models.Model):
    class Meta:
        verbose_name = 'Software product pricing'
        verbose_name_plural = 'Software products pricing'
        ordering = ['software', 'price']

    software = models.ForeignKey(SoftwareProduct, related_name='pricing')
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='name', unique_with='software')
    short_description = HTMLField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    per = models.CharField(max_length=255, null=True, blank=True,
                           help_text='Specify if pricing is per ... year, cpu, etc')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    is_best_seller = models.BooleanField(default=False)
    is_service = models.BooleanField(default=False)
    software_modules = models.ManyToManyField(SoftwareModule, related_name='pricings', verbose_name='Software modules')

    def __str__(self):
        return "%s %s for %s" % (self.software.name, self.name, self.price)

    def add_to_cart_url(self):
        return reverse('add-to-cart', kwargs={'software_slug': self.software.slug, 'slug': self.slug})



    @property
    def active_software_modules(self):
        return self.software_modules.filter(active=True)



