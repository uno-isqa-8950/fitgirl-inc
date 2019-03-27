from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import datetime, pytz
from account.models import Inactiveuser, CloneProgramInfo


def clone_program():
    try:
        program_rows = CloneProgramInfo.objects.filter(active=True)
    except CloneProgramInfo.DoesNotExist:
        exit(1)

    for row in program_rows:
        try:
            new_start_date = CloneProgramInfo.new_start_date
            program_to_clone = CloneProgramInfo.program_to_clone
            new_program = CloneProgramInfo.new_program
        except AttributeError:
            exit(1)

    local_timezone = pytz.timezone('America/Chicago')
    plus_one_week = datetime.timedelta(weeks=1)
    plus_one_day = datetime.timedelta(days=1)
    date_fields = new_start_date.split('-')
    new_start_datetime = datetime.datetime(int(date_fields[0]), int(date_fields[1]), int(date_fields[2]),
                                           tzinfo=local_timezone)
    new_program_slug = '-'.join(new_program.lower().split(' '))

    page_title = Program.objects.filter(id=program_to_clone).first().program_name
    page = Page.objects.filter(title=page_title).first()
    page.copy(recursive=True, update_attrs={'slug': new_program_slug,
                                            'title': new_program,
                                            'draft_title': new_program})

    page = Page.objects.filter(title=new_program).first()
    page_depth = page.depth
    weeks = [child for child in page.get_descendants() if child.depth == page_depth + 1]
    program_length = (len(weeks))

    program = Program()
    program.program_name = new_program
    program.program_start_date = new_start_datetime
    program.program_end_date = new_start_datetime + (plus_one_week * program_length) - plus_one_day
    program.created_date = datetime.datetime.now(local_timezone)
    program.updated_date = program.created_date
    program.save()

    for week in weeks:
        week_number = re.match('Week (\d+)$', week.title)[1]
        time_delta = (int(week_number) - 1) * plus_one_week
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
                    day.physicalpostpage.start_date = new_week_start_date + plus_one_day * 2
                    day.physicalpostpage.end_date = new_week_end_date + plus_one_day * 2
                elif str(day) == 'Thursday':
                    day.physicalpostpage.start_date = new_week_start_date + plus_one_day * 3
                    day.physicalpostpage.end_date = new_week_end_date + plus_one_day * 3
                elif str(day) == 'Friday':
                    day.physicalpostpage.start_date = new_week_start_date + plus_one_day * 4
                    day.physicalpostpage.end_date = new_week_end_date + plus_one_day * 4
                else:
                    print('Incorrect week title')

                day.physicalpostpage.save()



class Command(BaseCommand):
    def handle(self, **options):
        clone_program()

