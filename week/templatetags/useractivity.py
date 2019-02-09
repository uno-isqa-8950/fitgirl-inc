from django import template
from week.models import UserActivity
from account.models import Program, Parameters
import re
from string import capwords

register = template.Library()

@register.simple_tag
def is_week_done(user, item, page):
    program_name = re.search("pages\/([\w\d-]+)\/", page)[1]
    program_name = capwords(program_name).replace('-', ' ')
    program = Program.objects.filter(program_name=program_name).first()
    week = re.match('Week (\d+)$', item.text)[1]
    physical_count = UserActivity.objects.filter(user_id=user.id, Activity='physical', Week=week, program_id=program.program_id).count()
    nutrition_count = UserActivity.objects.filter(Activity='nutrition', Week=week, program_id=program.program_id).count()
    parameters = Parameters.objects.all().first()
    if nutrition_count >= parameters.nutrition_dayes_to_done and physical_count >= parameters.physical_days_to_done:
        return True
    else:
        return False