from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views
from django.views.decorators.cache import cache_page
from djangocms_blog.sitemaps import BlogSitemap

from website.views.common import sitemap

sitemaps = {'cmspages': CMSSitemap, 'blog': BlogSitemap}
urlpatterns = [
                            url(r'^backend/', include(admin.site.urls)),
                            url(r'^iprestrict/', include('iprestrict.urls', namespace='iprestrict')),
                            url(r'^deepexcavation/', include('website.urls')),
                            url(r'^accounts/', include('allauth.urls')),
                            url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
                            url(r'^sitemap\.xml$', cache_page(86400)(sitemap), {'sitemaps': sitemaps}),
                            ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception("Bad Request!")}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception("Permissin Denied")}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception("Page not Found")}),
        url(r'^500/$', default_views.server_error),
    ]

urlpatterns += [url(r'^', include('cms.urls'))]