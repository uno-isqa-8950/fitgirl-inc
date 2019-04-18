from django import template
from week.models import AnnouncementAlertPage
import datetime


register = template.Library()


@register.inclusion_tag('account/announcement_alert.html')
def announcement_alert():
    pass
