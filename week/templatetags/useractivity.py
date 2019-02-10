from django import template
from week.models import UserActivity
from account.models import Parameters, Profile, Program
import re

register = template.Library()

# Create a custom template tag to check if a user has completed the required activities to mark the week as done
# Uses the Parameters table to check what the required activities are and pulls data from UserActivity table to determine
# if the requisite amount of activities have been completed
@register.simple_tag
def is_week_done(user, item):
    profile = Profile.objects.filter(user_id=user.id).first()
    print(profile.program_id)
    program = Program.objects.filter(program_id=profile.program_id).first()
    week = re.match('Week (\d+)$', item.text)[1]
    physical_count = UserActivity.objects.filter(user_id=user.id, Activity='physical', Week=week, program_id=program.program_id).count()
    nutrition_count = UserActivity.objects.filter(Activity='nutrition', Week=week, program_id=program.program_id).count()
    parameters = Parameters()
    # Check if Parameters is populated. If not, add default row.
    if Parameters.objects.all().count() == 0:
        parameters.physical_days_to_done = 1
        parameters.nutrition_days_to_done = 1
        parameters.save()
    else:
        parameters = Parameters.objects.all().first()
    if nutrition_count >= parameters.nutrition_days_to_done and physical_count >= parameters.physical_days_to_done:
        return True
    else:
        return False

