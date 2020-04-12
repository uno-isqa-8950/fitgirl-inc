from import_export import resources
from .models import Profile, KindnessMessage
from django.contrib.auth.models import User

class ProfileResource(resources.ModelResource):
    class Meta:
        model = Profile
        fields = '__all__'

class KindnessMessageResource(resources.ModelResource):
    class Meta:
        model = KindnessMessage
        fields = '__all__'

class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = '__all__'