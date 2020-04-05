from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import DetailView
from sendfile import sendfile

from website.models import SoftwareProduct

__author__ = "ckopanos"


@method_decorator(never_cache, name='get')
@method_decorator(login_required, name='get')
class DownloadView(DetailView):

    model = SoftwareProduct
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(active=True)

    def get(self, request, *args, **kwargs):
        object = self.get_object()
        if not object.demo:
            raise Http404
        return sendfile(request, object.demo.path, attachment=True,
                        attachment_filename="%s%s" % (object.name, object.file_type))




