from django import template
from pages.models import OldUser

register = template.Library()

@register.filter(name='user_is_old')
def user_is_old(value):
    is_old_user = OldUser.objects.filter(login=value).exists()
    print(value)
    return is_old_user