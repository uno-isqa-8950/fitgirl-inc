from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import datetime, pytz, re
from account.models import Inactiveuser, CloneProgramInfo, Program
from wagtail.core.models import Page
from week.models import PhysicalPostPage
from django.core.mail import send_mail


def clone_program():
    try:
        program_rows = CloneProgramInfo.objects.filter(active=True)
    except CloneProgramInfo.DoesNotExist:
        exit(1)

    for row in program_rows:
        try:
            new_start_date = row.new_start_date
            program_to_clone = row.program_to_clone
            new_program = row.new_program
            user = row.user_id
        except AttributeError:
            exit(1)

        local_timezone = pytz.timezone('America/Chicago')
        plus_one_week = datetime.timedelta(weeks=1)
        plus_one_day = datetime.timedelta(days=1)
        # date_fields = new_start_date.split('-')
        new_start_datetime = datetime.datetime(new_start_date.year, new_start_date.month, new_start_date.day,
                                               hour=0, minute=0, second=1,
                                               tzinfo=local_timezone)
        new_program_slug = '-'.join(new_program.lower().split(' '))

        try:
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

            for week in weeks:
                week_number = re.match('Week (\d+)$', week.title)[1]
                time_delta = (int(week_number) - 1) * plus_one_week
                new_week_start_date = time_delta + new_start_datetime
                new_week_end_date = new_week_start_date + plus_one_day * 6
                week.weekpage.start_date = new_week_start_date
                week.weekpage.end_date = new_week_end_date
                week.weekpage.save()
                for activity in week.get_children():
                    # print("Activity " + str(activity))
                    for day in activity.get_children().type(PhysicalPostPage):
                        # print(week.title, str(day))
                        # print("start date " + str(day.physicalpostpage.start_date))

                        if str(day) == 'Monday':
                            day.physicalpostpage.start_date = new_week_start_date
                            day.physicalpostpage.end_date = new_week_end_date * 6
                        elif str(day) == 'Tuesday':
                            day.physicalpostpage.start_date = new_week_start_date + plus_one_day * 5
                            day.physicalpostpage.end_date = new_week_end_date + plus_one_day * 5
                        elif str(day) == 'Wednesday':
                            day.physicalpostpage.start_date = new_week_start_date + plus_one_day * 4
                            day.physicalpostpage.end_date = new_week_end_date + plus_one_day * 4
                        elif str(day) == 'Thursday':
                            day.physicalpostpage.start_date = new_week_start_date + plus_one_day * 3
                            day.physicalpostpage.end_date = new_week_end_date + plus_one_day * 3
                        elif str(day) == 'Friday':
                            day.physicalpostpage.start_date = new_week_start_date + plus_one_day * 2
                            day.physicalpostpage.end_date = new_week_end_date + plus_one_day * 2
                        else:
                            print('Incorrect week title')

                        day.physicalpostpage.save()

            row.active = False
            row.save()
            program.save()

            from_email = 'capstone18fa@gmail.com'
            content = 'Program ' + new_program + ' has been successfully created.'
            subject = 'Program cloning complete'

            user_obj = User.objects.get(id=user)
            email = user_obj.email
            send_mail(subject, content, from_email, [email])

        except Exception as e:
            print("An exception occurred ", e)


class Command(BaseCommand):
    def handle(self, **options):
        clone_program()
