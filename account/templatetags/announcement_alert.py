from django import template
from week.models import AnnouncementAlertPage
import datetime


register = template.Library()


@register.inclusion_tag('account/announcement_alert.html')
def announcement_alert():
    alert_warning = AnnouncementAlertPage.objects.all()
    for alerts in alert_warning:
        if alerts.display_warning == True:
            alert_data = alerts.announcements
            return {'alert_data':alert_data}