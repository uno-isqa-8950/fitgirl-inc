from django import template
from account.models import KindnessMessage
from django.contrib.auth.models import User

register = template.Library()


@register.inclusion_tag('account/../templates/email/user_message.html', takes_context=True)
def unread_message(context):
    request = context['request']
    user = User.objects.get(email=request.user.email)
    unread_count = KindnessMessage.objects.filter(to_user=user).filter(read_message=False).count()
    return {'unread_count': unread_count}
