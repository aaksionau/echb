from .models import Page


def add_menu_elements(request):
    """Adds context with menu items and current active page

    Arguments:
        request {[WSGIRequest]} -- [request from user]

    Returns:
        [dictionary] -- [dictionary with menu links and active page]
    """

    menu_links = Page.objects.filter(parent=None, visible_in_menu=True).order_by('order')
    path_parts = [slug for slug in request.path_info.split('/') if slug != '']

    # if length of splitted request is 0 it means that we are on home page
    if len(path_parts) == 0:
        path_parts.append('home')

    active_page = get_active_page(path_parts)

    context = {
        'menu_links': menu_links,
        'active_page': active_page,
    }
    return context


def get_active_page(request_slugs):
    """Get last available page from request slugs

    Arguments:
        request_slugs {list} -- [request slugs]

    Returns:
        [Page] -- [Page object]
    """

    request_slugs.reverse()
    page = None
    for slug in request_slugs:
        page = Page.objects.filter(slug=slug).select_related('parent').first()
        if page:
            break

    return page
