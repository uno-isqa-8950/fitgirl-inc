from django import template
from week.models import UserActivity, CustomFormSubmission
from account.models import Parameters, Profile, Program
import re

register = template.Library()

# Create a custom template tag to check if a user has completed the required activities to mark the week as done
# Uses the Parameters table to check what the required activities are and pulls data from UserActivity table to determine
# if the requisite amount of activities have been completed
@register.simple_tag
def is_week_done(user, item):
    profile = Profile.objects.filter(user_id=user.id).first()
    #print(profile.program_id)
    program = Program.objects.filter(id=profile.program_id).first()
    week = re.match('Week (\d+)$', item.text)[1]
    physical_count = UserActivity.objects.filter(user_id=user.id, Activity='physical', Week=week, program_id=program.id).count()
    nutrition_count = UserActivity.objects.filter(Activity='nutrition', Week=week, program_id=program.id).count()
    parameters = Parameters()
    # Check if Parameters is populated. If not, add default row.
    if Parameters.objects.filter(current_values=True).count() == 0:
        parameters.physical_days_to_done = 1
        parameters.nutrition_days_to_done = 1
        parameters.current_values = True
        parameters.save()
    else:
        parameters = Parameters.objects.filter(current_values=True).first()
    if nutrition_count >= parameters.nutrition_days_to_done and physical_count >= parameters.physical_days_to_done:
        return True
    else:
        return False

@register.simple_tag
def nutrition_activities_done(page, user):
    child_pages = page.get_children()
    count = 0
    for question in child_pages:
        if CustomFormSubmission.objects.filter(page_id=question.id, user_id=user.id).count() > 0:
            count += 1
    return count

@register.simple_tag
def nutrition_activity_count(page):
    children = page.get_children()
    return children.count()

@register.simple_tag
def is_nutrition_page(page):
    if re.search('Nutrition', page.title):
        return True
    else:
        return False

@register.simple_tag
def is_physical_page(page):
    if re.search('Physical', page.title):
        return True
    else:
        return False

@register.simple_tag
def physical_activity_done(page, user):
    if CustomFormSubmission.objects.filter(page_id=page.id, user_id=user.id).count() > 0:
        return True
    else:
        return False
