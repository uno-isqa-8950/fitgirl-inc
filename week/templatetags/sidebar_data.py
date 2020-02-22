from django import template
from week.models import SidebarContentPage,SidebarImagePage

register = template.Library()


@register.inclusion_tag('week/announcement.html')
def sidebar():
    sidebar_data = SidebarContentPage.objects.get()

    return {'sidebar_data':sidebar_data}

@register.inclusion_tag('week/advertisement.html')
def sidebarimage():
    sidebar_image = SidebarImagePage.objects.get()

    return {'sidebar_image':sidebar_image}