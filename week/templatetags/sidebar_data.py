from django import template
from week.models import SidebarContentPage

register = template.Library()

@register.inclusion_tag('week/announcement.html')
def sidebar():
    sidebar_data = SidebarContentPage.objects.get()

    return {'sidebar_data':sidebar_data}
