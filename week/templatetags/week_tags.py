from django import template
from week.models import BoilerPlate

register = template.Library()

...

# Advert snippets
@register.inclusion_tag('tags/boilerplate.html', takes_context=True)
def boilerplate(context):
    return {
        'adverts': BoilerPlate.objects.all(),
        'request': context['request'],
    }