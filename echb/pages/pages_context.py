from .models import Page
from django.conf.urls import url
from helpers.utils import BreadCrumLink

def add_menu_elements(request):
    menu_links = Page.objects.filter(parent=None, visible_in_menu=True).order_by('order')
    path_parts = request.path_info.split('/')
    active_page = None
    parent = None
    if len(path_parts) > 2:
        page = Page.objects.filter(slug=path_parts[1]).select_related('parent').first()
        if page:
            active_page = page
    elif len(path_parts) == 2:
        active_page = menu_links.get(slug='home')

    context = {
        'menu_links': menu_links,
        'active_page': active_page,
    }
    return context