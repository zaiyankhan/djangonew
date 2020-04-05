from colorfield.fields import ColorField
from filer.fields.image import FilerImageField

__author__ = 'ckopanos'

from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.extensions import PageExtension
from cms.extensions.extension_pool import extension_pool


class HeaderBackgroundExtension(PageExtension):

    class Meta(PageExtension.Meta):
        verbose_name = "Page background"
        verbose_name_plural = "Page backgrounds"

    image = FilerImageField(null=True, blank=True, related_name="page_header",verbose_name=_("Page header"))

extension_pool.register(HeaderBackgroundExtension)


class HighlightedMenuExtension(PageExtension):
    color = ColorField(max_length=10, null=True, blank=True)
    button_like = models.BooleanField(default=False)
    button_background_color = ColorField(null=True, blank=True)


extension_pool.register(HighlightedMenuExtension)