from django.conf.urls import url, include

__author__ = "ckopanos"

urlpatterns = [
    url(r'^software/', include('website.urls.software')),
    url(r'^clients/', include('website.urls.user')),
    url(r'^cart/', include('website.urls.shopping')),
    url('^payments/', include('payments.urls'))
]