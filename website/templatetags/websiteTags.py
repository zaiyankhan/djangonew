from carton.cart import Cart
from django import template

register = template.Library()
@register.inclusion_tag('includes/pagination.html', takes_context=True)
def website_pagination(context, page, begin_pages=1, end_pages=1,
                       before_pages=2, after_pages=2,
                       template='includes/pagination.html'):
    """
    Return a Digg-like pagination,
    by splitting long list of page into 3 blocks of pages.
    """
    GET_string = ''
    for key, value in context['request'].GET.items():
        if key != 'page':
            GET_string += '&%s=%s' % (key, value)

    begin = list(page.paginator.page_range[:begin_pages])
    end = list(page.paginator.page_range[-end_pages:])
    middle = list(page.paginator.page_range[
                  max(page.number - before_pages - 1, 0):page.number + after_pages])

    if set(begin) & set(middle):  # [1, 2, 3], [2, 3, 4], [...]
        begin = sorted(set(begin + middle))  # [1, 2, 3, 4]
        middle = []
    elif begin[-1] + 1 == middle[0]:  # [1, 2, 3], [4, 5, 6], [...]
        begin += middle  # [1, 2, 3, 4, 5, 6]
        middle = []
    elif middle[-1] + 1 == end[0]:  # [...], [15, 16, 17], [18, 19, 20]
        end = middle + end  # [15, 16, 17, 18, 19, 20]
        middle = []
    elif set(middle) & set(end):  # [...], [17, 18, 19], [18, 19, 20]
        end = sorted(set(middle + end))  # [17, 18, 19, 20]
        middle = []

    if set(begin) & set(end):  # [1, 2, 3], [...], [2, 3, 4]
        begin = sorted(set(begin + end))  # [1, 2, 3, 4]
        middle, end = [], []
    elif begin[-1] + 1 == end[0]:  # [1, 2, 3], [...], [4, 5, 6]
        begin += end  # [1, 2, 3, 4, 5, 6]
        middle, end = [], []

    return {'template': template,
            'page': page,
            'begin': begin,
            'middle': middle,
            'end': end,
            'GET_string': GET_string}


def background(page):
    if page.headerbackgroundextension:
        return page.headerbackgroundextension
    if page.is_home or page.parent is None:
        return None
    return background(page.parent)

@register.assignment_tag(takes_context=True)
def page_background(context):
    request = context['request']
    try:
        page = request.current_page
        return background(page)
    except Exception:
        return None


@register.simple_tag(takes_context=True)
def shopping_cart(context):
    if 'request' in context:
        session = context['request'].session
        if 'start' not in session:
            session['start'] = True
        return Cart(context['request'].session)
    return None