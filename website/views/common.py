import warnings

import six
from django.contrib.sitemaps.views import x_robots_tag
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import mail_managers
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.http import Http404
from django.http import JsonResponse
from django.template import RequestContext
from django.template.defaultfilters import striptags
from django.template.loader import get_template
from django.template.response import TemplateResponse
from django.views.decorators.cache import cache_control, cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from website.forms.contact import ContactForm


@require_POST
def contact(request):
    if not request.is_ajax():
        raise Http404
    formsent = False
    form = ContactForm(data=request.POST)
    if form.is_valid():
        currentSite = get_current_site(request)
        subject = u'Contact form request from %(site)s' % {'site': currentSite.name}
        html = get_template('email/other/contact.html')
        d = RequestContext(request, {"contact_details": form.cleaned_data})
        html = html.render(d)
        plaintext = striptags(html)
        mail_managers(subject, plaintext, fail_silently=True, html_message=html)
        formsent = True
        return JsonResponse({'success': formsent})


@x_robots_tag
@cache_control(public=True)
@cache_page(3600 * 24)
def sitemap(request, sitemaps, section=None,
            template_name='sitemap.xml', content_type='application/xml',
            mimetype=None):
    if mimetype:
        warnings.warn("The mimetype keyword argument is deprecated, use "
                      "content_type instead", PendingDeprecationWarning, stacklevel=2)
        content_type = mimetype

    req_protocol = 'https' if request.is_secure() else 'http'
    req_site = get_current_site(request)

    if section is not None:
        if section not in sitemaps:
            raise Http404("No sitemap available for section: %r" % section)
        maps = [sitemaps[section]]
    else:
        maps = list(six.itervalues(sitemaps))
    page = request.GET.get("p", 1)

    urls = []
    for site in maps:
        try:
            if callable(site):
                site = site()
            urls.extend(site.get_urls(page=page, site=req_site,
                                      protocol=req_protocol))
        except EmptyPage:
            raise Http404("Page %s empty" % page)
        except PageNotAnInteger:
            raise Http404("No page '%s'" % page)
    return TemplateResponse(request, template_name, {'urlset': urls},
                            content_type=content_type)
