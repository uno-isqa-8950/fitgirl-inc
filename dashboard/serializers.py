from rest_framework import serializers
from week.models import UserActivity

class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = ['id', 'program', 'Activity', 'DayOfWeek']