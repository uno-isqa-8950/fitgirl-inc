from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import datetime
from django.core.mail import send_mail


def user_inactivity():
    users = User.objects.filter(last_login__lte=datetime.datetime.now() - datetime.timedelta(days=7)).filter(is_superuser=False)
    for user in users:
        email = user.email
        subject = 'Hello Scheduler'
        message = 'This is a Scheduler message'
        send_mail(subject,message,'capstone18fa@gmail.com',[email])


class Command(BaseCommand):
    def handle(self, **options):
        user_inactivity()