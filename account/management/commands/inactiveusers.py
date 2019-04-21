from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import datetime
from django.core.mail import send_mail
from week.models import EmailTemplates
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from account.models import Inactiveuser


def user_inactivity():
    try:
        latest_date = Inactiveuser.objects.latest()
        latest_set_date = latest_date.set_days
    except Inactiveuser.DoesNotExist:
        latest_set_date = 7

    users = User.objects.filter(last_login__lte=datetime.datetime.now() - datetime.timedelta(days=latest_set_date)).filter(is_superuser=False).filter(is_active=True)
    from_email = 'capstone18fa@gmail.com'
    # subject = EmailTemplates.objects.filter(subject_inactivity)
    # subject = 'Inactive for long time'
    user_inactivity = "True"
    content = EmailTemplates.objects.get()
    # print(content.subject_for_inactivity)
    subject = content.subject_for_inactivity
    html_message = render_to_string('account/../../templates/other/../../templates/email/group_email_template.html',
                                    {'content': content, 'user_inactivity': user_inactivity})


    plain_message = strip_tags(html_message)
    for user in users:
        email = user.email
        send_mail(subject, plain_message, from_email, [email], html_message=html_message)



class Command(BaseCommand):
    def handle(self, **options):
        user_inactivity()

