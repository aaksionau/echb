from django import template

register = template.Library()


@register.filter
def videos_in_category(video_list, category):
    return list(video_list[category])
