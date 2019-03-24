from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import datetime
from django.core.mail import send_mail
from week.models import EmailTemplates
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from account.models import RewardsNotification


def rewards_notification():
    users = User.objects.all().filter(is_superuser=False).filter(is_active=True)

    rewards_notification = "True"

    messages = EmailTemplates.objects.get()

    subject = messages.subject_for_rewards_notification

    html_message = render_to_string('account/group_email_template.html',
                                    {'content': messages, 'rewards_notification': rewards_notification})

    plain_message = strip_tags(html_message)

    try:
        milestones = RewardsNotification.objects.latest()
        set_point1 = milestones.Rewards_milestone_1
        set_point2 = milestones.Rewards_milestone_2
        set_point3 = milestones.Rewards_milestone_3
        set_point4 = milestones.Rewards_milestone_4
    except RewardsNotification.DoesNotExist:
        set_point1 = 25
        set_point2 = 50
        set_point3 = 75
        set_point4 = 100

    for user in users:

        if user.profile.points == set_point1 or user.profile.points == set_point2 or user.profile.points == set_point3 or user.profile.points == set_point4:
            from_email = 'capstone18fa@gmail.com'
            email = user.email
            print(email)
            send_mail(subject,plain_message,from_email,[email],html_message=html_message)



class Command(BaseCommand):
    def handle(self,**options):
        rewards_notification()

