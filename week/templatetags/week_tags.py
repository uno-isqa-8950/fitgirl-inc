from django import template
from week.models import BoilerPlate

register = template.Library()

...

# Advert snippets
@register.inclusion_tag('tags/boilerplate.html', takes_context=True)
def boilerplate(context):
    return {
        'boilerplates': BoilerPlate.objects.all(),
        'request': context['request'],
    }