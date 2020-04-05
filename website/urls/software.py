from django.conf.urls import  url

from website.views.software import DownloadView

urlpatterns = [
                       url(r'^download/(?P<slug>[\w\s\d_-]+)$', DownloadView.as_view(), {},
                           'download-software'),
                ]
