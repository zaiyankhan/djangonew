from django.conf.urls import include, url
from django.views.decorators.cache import cache_page

from website.views import contact
from website.views import TwitterFeedView

urlpatterns = [
    url(r'^twitter-feed/$',
        cache_page(3600)(TwitterFeedView.as_view()),
        name='twitter-feed'),
    url(r'^contact-us/$', contact, {}, name='contact-form'),
              ]