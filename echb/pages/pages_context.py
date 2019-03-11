from .models import Page


class ShortPage:
    def __init__(self, title, slug):
        self.title = title
        self.slug = slug

    def __str__(self):
        return self.title


def add_menu_elements(request):
    menu_links = Page.objects.filter(parent=None, visible_in_menu=True).order_by('order')
    path_parts = [slug for slug in request.path_info.split('/') if slug != '']

    # if length of splitted request is 0 it means that we are on home page
    if len(path_parts) == 0:
        path_parts.append('home')

    if 'admin' in path_parts:
        return {}

    path_parts.reverse()
    active_page = get_active_page(path_parts)
    page = Page.objects.select_related('parent').get(slug=active_page.slug)
    breadcrumbs = get_breadcrumbs(page, [])

    context = {
        'menu_links': menu_links,
        'active_page': active_page,
        'bread_crumbs': breadcrumbs
    }
    return context


def get_breadcrumbs(current_page, breadcrumbs):
    short_page = ShortPage(current_page.title, f'{current_page.slug}')
    breadcrumbs.append(short_page)
    if len(breadcrumbs) >= 1:
        parent_slug = current_page.slug
        for i in range(len(breadcrumbs)-1):
            breadcrumbs[i].slug = f'{parent_slug}/{breadcrumbs[i].slug}'

    if current_page.parent is None:
        breadcrumbs.reverse()
        return breadcrumbs

    current_page = Page.objects.get(slug=current_page.parent.slug)
    return get_breadcrumbs(current_page, breadcrumbs)


def get_active_page(request_slugs):
    page = None
    for slug in request_slugs:
        page = Page.objects.filter(slug=slug).select_related('parent')
        if page:
            page = page.first()
            break

    return page
