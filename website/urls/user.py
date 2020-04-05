from django.conf.urls import url, include

from website.views.user import UserProfileView, AccountDetailsView

urlpatterns = [
    url(r'^profile/$', UserProfileView.as_view(), {}, 'user-profile'),
    url(r'^account-details/$', AccountDetailsView.as_view(), {}, 'user-account-details'),
    url(r'^support/', include('helpdesk.urls')),
]
