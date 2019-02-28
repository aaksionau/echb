from .models import Page


def add_menu_elements(request):
    menu_links = Page.objects.filter(parent=None, visible_in_menu=True).order_by('order')
    path_parts = [slug for slug in request.path_info.split('/') if slug != '']

    # if length of splitted request is 0 it means that we are on home page
    if len(path_parts) == 0:
        path_parts.append('home')

    path_parts.reverse()
    current_page_slug = path_parts[0]
    page = Page.objects.select_related('parent').get(slug=current_page_slug)
    breadcrumbs = get_breadcrumbs(page, [])
    active_page = get_active_page(path_parts)

    context = {
        'menu_links': menu_links,
        'active_page': active_page,
        'bread_crumbs': breadcrumbs
    }
    return context


def get_breadcrumbs(current_page, breadcrumbs):
    breadcrumbs.append(current_page)

    if current_page.parent is None:
        breadcrumbs.reverse()
        return breadcrumbs

    current_page = Page.objects.get(slug=current_page.parent.slug)
    return get_breadcrumbs(current_page, breadcrumbs)


def get_active_page(request_slugs):
    request_slugs.reverse()
    page = None
    for slug in request_slugs:
        page = Page.objects.filter(slug=slug).select_related('parent').first()
        if page:
            break

    return page
