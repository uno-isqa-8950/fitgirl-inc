from django import template
from account.models import RewardCategory, RewardItem, Profile, Parameters
from django.conf import settings
from django.core import exceptions

register = template.Library()

# Create a custom template tag to check if a user has completed the required activities to mark the week as done
# Uses the Parameters table to check what the required activities are and pulls data from UserActivity table to determine
# if the requisite amount of activities have been completed
@register.simple_tag
def reward_categories():
    items = RewardItem.objects.filter(qty_available__gt=0)
    categories = set()
    for item in items:
        try:
            category = RewardCategory.objects.get(id=item.category_id)
            categories.add(category)
        except exceptions.ObjectDoesNotExist:
            pass
    return categories

@register.simple_tag
def all_reward_categories():
    categories = RewardCategory.objects.all()
    return categories

@register.simple_tag
def reward_items(category):
    items = RewardItem.objects.filter(category_id=category, qty_available__gt=0)
    return items

@register.simple_tag
def category_name(category_id):
    categories = RewardCategory.objects.get(id=category_id)
    return categories

@register.simple_tag
def all_reward_items():
    items = RewardItem.objects.all()
    return items

@register.simple_tag
def media_url():
    return settings.STATIC_URL + '..' + settings.MEDIA_URL

@register.simple_tag
def available_points(user):
    try:
        points = Profile.objects.get(user_id=user).points
    except Exception as e:
        print(e)
        points = 0
    return points

@register.simple_tag
def are_rewards_active():
    try:
        settings = Parameters.objects.get(current_values=True)
        active = settings.rewards_active
    except AttributeError:
        print('Error in are_rewards_active')
        return False

    return active
