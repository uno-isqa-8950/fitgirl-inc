from wagtail.core import hooks
from wagtail.admin import widgets as wagtailadmin_widgets
import re
from datetime import datetime, timedelta
from week.models import WeekPage, ModelIndexPage, PhysicalPostPage
import pytz
from account.models import Program

@hooks.register('construct_main_menu')
def hide_explorer_menu_item_from_frank(request, menu_items):
    menu_items[:] = [item for item in menu_items ]

@hooks.register('after_copy_page')
def after_copy_page(request, page_class, new_page_class):
    local_timezone = pytz.timezone('America/Chicago')
    plus_one_week = timedelta(weeks=1)
    plus_one_day = timedelta(days=1)
    #new_start_date = input("Enter new start date: ")
    new_start_date = '2/4/2019'
    date_fields = new_start_date.split('/')
    new_start_datetime = datetime(int(date_fields[2]), int(date_fields[0]), int(date_fields[1]), tzinfo=local_timezone)
    parent = new_page_class.get_parent()
    grandparent = parent.get_parent()
    children = new_page_class.get_children()

    if str(grandparent) == 'Root':
        program = Program()
        program.program_name = new_page_class
        program.program_start_date = new_start_datetime
        program.program_end_date = new_start_datetime + plus_one_week * 13 - plus_one_day
        program.created_date = datetime.now(local_timezone)
        program.updated_date = program.created_date
        program.save()

        weeks = children.type(WeekPage)
        for week in weeks:
            week_number = re.match('Week (\d+)$', week.title)[1]
            time_delta = (int(week_number)-1) * plus_one_week
            new_week_start_date = time_delta + new_start_datetime
            new_week_end_date = new_week_start_date + plus_one_day * 6
            week.weekpage.start_date = new_week_start_date
            week.weekpage.end_date = new_week_end_date
            week.weekpage.save()
            for activity in week.get_children():
                print("Activity " + str(activity))
                for day in activity.get_children().type(PhysicalPostPage):
                    print(week.title, str(day))
                    print("start date " + str(day.physicalpostpage.start_date))

                    if str(day) == 'Monday':
                        day.physicalpostpage.start_date = new_week_start_date
                        day.physicalpostpage.end_date = new_week_end_date
                    elif str(day) == 'Tuesday':
                        day.physicalpostpage.start_date = new_week_start_date + plus_one_day
                        day.physicalpostpage.end_date = new_week_end_date + plus_one_day
                    elif str(day) == 'Wednesday':
                        day.physicalpostpage.start_date = new_week_start_date + plus_one_day*2
                        day.physicalpostpage.end_date = new_week_end_date + plus_one_day*2
                    elif str(day) == 'Thursday':
                        day.physicalpostpage.start_date = new_week_start_date + plus_one_day*3
                        day.physicalpostpage.end_date = new_week_end_date + plus_one_day*3
                    elif str(day) == 'Friday':
                        day.physicalpostpage.start_date = new_week_start_date + plus_one_day*4
                        day.physicalpostpage.end_date = new_week_end_date + plus_one_day*4
                    else:
                        print('Incorrect week title')

                    day.physicalpostpage.save()

    return True

@hooks.register('register_page_listing_more_buttons')
def page_listing_more_buttons(page, page_perms, is_parent=False):
    yield wagtailadmin_widgets.Button(
        'Clone',
        '/cloneprogram',
        priority=60
    )