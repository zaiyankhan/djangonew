__author__ = 'ckopanos'
from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    name = 'website'
    verbose_name = "DeepExcavation"


from cms.apps import CMSConfig
from django.apps import AppConfig
from filer.apps import FilerConfig


class CMSAppConfig(CMSConfig):
    verbose_name = 'CMS'


class DjangoFilerConfig(FilerConfig):
    verbose_name = 'Multimedia Library'


class CMSPluginFilerImageConfig(AppConfig):
    name = 'cmsplugin_filer_image'
    verbose_name = 'Thumbnail options'
