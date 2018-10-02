from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

EVENT = (
    (1, _("8-10")),
    (2, _("11-13")),
)


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

class RegisterUser(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=True, null=None)
    first_name = models.CharField(max_length=50, default=None)
    last_name = models.CharField(max_length=50, default=None)
    is_active = models.BooleanField(_('active'), default =True)
    program = models.CharField(max_length=50, default='Test')



class Profile(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default='profile_image/default.jpg', upload_to='profile_image', blank=True)
    # first_name = models.CharField(max_length=50, default=None)
    # last_name = models.CharField(max_length=50, default=None)
    bio = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    zip = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=25, blank=True, null=True)
    state = models.CharField(max_length=25, blank=True, null=True)
    day_phone = models.IntegerField(blank=True, null=True)
    eve_phone = models.IntegerField(blank=True, null=True)
    age_group = models.IntegerField(choices=EVENT, blank=True, null=True, default=None)
    school = models.CharField(max_length=50, blank=True, null=True)


    def __str__(self):
        return f'{self.user.username} Profile'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


