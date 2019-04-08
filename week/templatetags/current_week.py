from django import template
from week.models import WeekPage
import datetime

register = template.Library()

@register.inclusion_tag('week/this_week.html')
def current_week():
    today = datetime.date.today()
    weeks = WeekPage.objects.filter(end_date__gte=today, start_date__lte=today)
    for this_week in weeks:
        print(this_week.title)
        todays_week = this_week.title.lower()
        print(todays_week)
        week_gap_pos = todays_week.find(" ")
        new_week_str = todays_week[0:week_gap_pos] + '-' + todays_week[week_gap_pos:]
        print(new_week_str)
        current_week_name = new_week_str.replace(" ", "")
        return {'current_week_name':current_week_name}