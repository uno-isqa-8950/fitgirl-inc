from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Program(models.Model):
    #program_id = models.AutoField(null=False, primary_key=True)
    program_name = models.CharField(max_length=20, null=False)
    program_start_date = models.DateField(null=False, blank=False)
    program_end_date = models.DateField(null=False, blank=False)
    created_date = models.DateTimeField(default=timezone.now, blank=True)
    updated_date = models.DateTimeField(auto_now_add=True, null=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.program_name)

class ValidUser(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=False, null=True)
    first_name = models.CharField(max_length=50, blank=False, null=True)#default='None')
    last_name = models.CharField(max_length=50, blank=False, null=True)#default='None')
    is_active = models.BooleanField(_('active'), default =True)
    program = models.CharField(max_length=50, default='Test')



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=False, null=True)#default='None')
    last_name = models.CharField(max_length=50, blank=False, null=True)#default='None')
    #email = models.EmailField(blank=True, null=None)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(default='profile_image/default.jpg',upload_to='profile_image',blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
