from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from dashboard.serializers import UserActivitySerializer
from week.models import UserActivity


# Create your views here.
class UserActivityViewSet(viewsets.ModelViewSet):

    #check permission
    permission_classes = (
        IsAuthenticated,
    )
    queryset = UserActivity.objects.all()
    serializer_class = UserActivitySerializer
    lookup_field = 'id'
