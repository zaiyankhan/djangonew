from aldryn_bootstrap3 import model_fields
from cms.models import CMSPlugin
from colorfield.fields import ColorField
from django.db import models
from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField

__author__ = "ckopanos"


class SoftwareDownloadPlugin(CMSPlugin):

    software = models.ForeignKey('SoftwareProduct', blank=False,
                                 help_text='Select a specific software product')
    button_color = ColorField(blank=True)
    button_text_color = ColorField(blank=True)

    cmsplugin_ptr = model_fields.CMSPluginField()

    def __str__(self):
        return 'Download: %s' % self.software.name


class SoftwarePricingPlugin(CMSPlugin):
    template = models.CharField(choices=(('vertical', 'Vertical'), ('horizontal', 'Horizontal')),
                                max_length=20, default='vertical')
    software = models.ForeignKey('SoftwareProduct', blank=False,
                                 help_text='Select a specific software product')
    include_modules = models.BooleanField(default=False)
    buy_now_button_color = ColorField(blank=True)
    buy_now_text_color = ColorField(blank=True)
    add_to_cart_button_color = ColorField(blank=True)
    add_to_cart_text_color = ColorField(blank=True)
    show_buy_now_button = models.BooleanField(default=True)
    show_add_to_cart_button = models.BooleanField(default=True)
    cmsplugin_ptr = model_fields.CMSPluginField()

    def __str__(self):
        return 'Product Pricing: %s' % self.software.name


class SoftwareSpecificPricingPlugin(CMSPlugin):
    template = models.CharField(choices=(('vertical', 'Vertical'), ('horizontal', 'Horizontal')),
                                max_length=20, default='vertical')
    pricing = models.ForeignKey('SoftwareProductPricing', blank=False,
                                 help_text='Select a specific pricing for a software product')
    include_modules = models.BooleanField(default=False)
    buy_now_button_color = ColorField(blank=True)
    buy_now_text_color = ColorField(blank=True)
    add_to_cart_button_color = ColorField(blank=True)
    add_to_cart_text_color = ColorField(blank=True)
    show_buy_now_button = models.BooleanField(default=True)
    show_add_to_cart_button = models.BooleanField(default=True)
    cmsplugin_ptr = model_fields.CMSPluginField()

    def __str__(self):
        return 'Pricing for %s %s' % (self.pricing.software.name, self.pricing.name)


class PromotionBoxPlugin(CMSPlugin, model_fields.LinkMixin):

    title = models.CharField(max_length=255)
    info = HTMLField(null=True, blank=True)
    link_text = models.CharField(max_length=255, null=True, blank=True)
    icon = model_fields.Icon()
    image = FilerImageField(null=True, blank=True, related_name="promotional_box_images")
    apply_hover_effect = models.BooleanField(default=False)
    button_color = ColorField(blank=True)
    button_text_color = ColorField(blank=True)
    is_active = models.BooleanField(default=False, help_text='Only applicable with is apply hover effect')
    cmsplugin_ptr = model_fields.CMSPluginField()
    background_color = ColorField(null=True, blank=True)


class TestimonialsBoxPlugin(CMSPlugin):
    title = models.CharField(max_length=255)
    info = models.CharField(max_length=255, null=True, blank=True)
    who = models.CharField(max_length=255, null=True, blank=True)
    company = models.CharField(max_length=255, null=True, blank=True)
    image = FilerImageField(null=True, blank=True, related_name="testimonial_box_images")
    cmsplugin_ptr = model_fields.CMSPluginField()


class ColoredAreaBox(CMSPlugin):
    include_container = models.BooleanField(default=True, help_text='Leave cheched only for full width areas')
    style = models.CharField(choices=(
        ('more-features', 'Dark brown'),
        ('more-info', 'Light brown'),
        ('testimonials', 'Mpez'),
        ('pricing', 'White padded'),
        ('', 'Plain')
    ), default='.more-features', max_length=50)
    background_color = ColorField(blank=True, help_text='Use specific color to override style background color')
    padding = models.CharField(null=True, blank=True, help_text="css padding", max_length=100)


class DownloadSoftwareButton(CMSPlugin):
    software = models.ForeignKey('SoftwareProduct', blank=False,
                                 help_text='Select a specific software product')
    title = models.CharField(max_length=100, default='Download free trial')
    css_class = models.CharField(max_length=100, default='btn btn-danger btn-lg')
    button_color = ColorField(blank=True)
    button_text_color = ColorField(blank=True)
    cmsplugin_ptr = model_fields.CMSPluginField()

    def __str__(self):
        return 'Download button for: %s' % self.software.name
