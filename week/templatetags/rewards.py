from django import template
from account.models import RewardCategory, RewardItem

register = template.Library()

# Create a custom template tag to check if a user has completed the required activities to mark the week as done
# Uses the Parameters table to check what the required activities are and pulls data from UserActivity table to determine
# if the requisite amount of activities have been completed
@register.simple_tag
def reward_categories():
    categories = RewardCategory.objects.all()
    return categories


@register.simple_tag
def reward_items(category):
    items = RewardItem.objects.filter(category=category)
    return items
