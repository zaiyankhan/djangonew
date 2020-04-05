# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from djangocms_blog.models import Post

from website.models import PromotionBoxPlugin, ColoredAreaBox
from website.models import SoftwareDownloadPlugin
from website.models import SoftwarePricingPlugin
from website.models import SoftwareSpecificPricingPlugin
from website.models import TestimonialsBoxPlugin, DownloadSoftwareButton


class WebsitePlugin(CMSPluginBase):

    module = 'DeepExcavation'
    text_enabled = False
    cache = True


class SoftwarePricingPlugin(WebsitePlugin):

    render_template = 'software/pricing/item.html'
    name = 'Software product pricing options'
    model = SoftwarePricingPlugin
    cache = True

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['software'] = instance.software
        return context


class SoftwareSpecificPricingPlugin(WebsitePlugin):
    render_template = 'software/pricing/specific_item.html'
    name = 'Pricing option for a software product'
    model = SoftwareSpecificPricingPlugin
    cache = True

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['pricing'] = instance.pricing
        return context

class SoftwareDownloadPlugin(WebsitePlugin):
    render_template = 'software/download/item.html'
    name = 'Software download'
    model = SoftwareDownloadPlugin
    cache = True

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['software'] = instance.software
        return context


class PromotionalBoxPlugin(WebsitePlugin):
    render_template = 'plugins/promotional_box.html'
    name = 'Promotional box'
    model = PromotionBoxPlugin
    change_form_template = 'admin/aldryn_bootstrap3/base.html'
    cache = True

    def render(self, context, instance, placeholder):
        context['promotional_box'] = instance
        return context


class TestimonialBoxPlugin(WebsitePlugin):
    render_template = 'plugins/testimonial_box.html'
    name = 'Testimonial box'
    model = TestimonialsBoxPlugin
    change_form_template = 'admin/aldryn_bootstrap3/base.html'
    cache = True

    def render(self, context, instance, placeholder):
        context['testimonial_box'] = instance
        return context

class ColoredAreaPlugin(WebsitePlugin):
    render_template = 'plugins/colored_area.html'
    allow_children = True
    cache = False
    name = 'Content area'
    model = ColoredAreaBox


class DownloadSoftwareButtonPlugin(WebsitePlugin):
    render_template = 'plugins/download_software_button.html'
    allow_children = True
    cache = False
    name = 'Download software button'
    model = DownloadSoftwareButton



plugin_pool.register_plugin(SoftwarePricingPlugin)
plugin_pool.register_plugin(SoftwareSpecificPricingPlugin)
plugin_pool.register_plugin(SoftwareDownloadPlugin)
plugin_pool.register_plugin(PromotionalBoxPlugin)
plugin_pool.register_plugin(TestimonialBoxPlugin)
plugin_pool.register_plugin(ColoredAreaPlugin)
plugin_pool.register_plugin(DownloadSoftwareButtonPlugin)