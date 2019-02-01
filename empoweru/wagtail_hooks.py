from wagtail.core import hooks
from wagtail.admin import widgets as wagtailadmin_widgets
import re, datetime
from week.models import WeekPage, ModelIndexPage, PhysicalPostPage
from django.utils import timezone


@hooks.register('construct_main_menu')
def hide_explorer_menu_item_from_frank(request, menu_items):
    menu_items[:] = [item for item in menu_items ]

@hooks.register('after_copy_page')
def after_copy_page(request, page_class, new_page_class):
    plus_one_week = datetime.timedelta(weeks=1)
    plus_one_day = datetime.timedelta(days=1)
    new_start_date = input("Enter new start date: ")
    date_fields = new_start_date.split('/')
    new_start_datetime = datetime.datetime(int(date_fields[2]), int(date_fields[0]), int(date_fields[1]), tzinfo = datetime.tzinfo.tzname('America/Chicago'))
    parent = new_page_class.get_parent()
    grandparent = parent.get_parent()
    descendants = new_page_class.get_children()

    if re.match('Week ', str(page_class)):
        days = descendants
    if str(grandparent) == 'Root':
        weeks = descendants.type(WeekPage)
        for week in weeks:
            print(week.title, str(week.weekpage.start_date), str(week.weekpage.end_date))
            week_number = re.match('Week (\d+)$', week.title)[1]
            print(week_number)
            time_delta = int(week_number) * plus_one_week
            new_week_start_date = time_delta + new_start_datetime
            week.weekpage.start_date = new_week_start_date
            week.weekpage.save()
            for activity in week.get_children():
                print("Activity " + str(activity))
                for day in activity.get_children().type(PhysicalPostPage):
                    print(week.title, str(day))
                    print("start date " + str(day.physicalpostpage.start_date))
    return True

@hooks.register('register_page_listing_more_buttons')
def page_listing_more_buttons(page, page_perms, is_parent=False):
    yield wagtailadmin_widgets.Button(
        'a dropdown button',
        '/pages/week_18',
        priority=60
    )