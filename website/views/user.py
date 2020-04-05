from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView, UpdateView

from website.forms.user import UserChangeForm
from website.models import AppUser


__author__ = "ckopanos"


@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class UserProfileView(TemplateView):

    template_name = 'account/profile.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class AccountDetailsView(UpdateView):

    model = AppUser
    form_class = UserChangeForm
    template_name = 'account/account_details.html'

    def get_object(self, queryset=None):
        return self.request.user





