from django import template
from account.models import Program
import datetime

register = template.Library()

@register.inclusion_tag('week/this_program.html')
def current_program():
    today = datetime.date.today()
    programs = Program.objects.filter(program_start_date__lt=today).filter(program_end_date__gte=today)
    for program in programs:
        current_program = program.program_name
        current_program_lower = current_program.lower()
        gap_pos = current_program_lower.find(" ")
        new_str = current_program_lower[0:gap_pos] + '-' + current_program_lower[gap_pos:]
        current_program_name = new_str.replace(" ", "")
        return {'current_program_name':current_program_name}