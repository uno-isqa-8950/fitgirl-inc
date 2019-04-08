from django import template
from week.models import AnnouncementAlertPage
import datetime


register = template.Library()


@register.inclusion_tag('account/announcement_alert.html')
def announcement_alert():
    today = datetime.date.today()
    print(today)
    alert_message = AnnouncementAlertPage.objects.filter(start_date__lte=today) & AnnouncementAlertPage.objects.filter(end_date__gte=today)
    for alerts in alert_message:
        alert_data = alerts.announcements
        return {'alert_data':alert_data}