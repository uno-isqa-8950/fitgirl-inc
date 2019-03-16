from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

EVENT = (
    (1, _("8-10")),
    (2, _("11-13")),
)


class Program(models.Model):
    #program_id = models.AutoField(null=False, primary_key=True)
    program_name = models.CharField(max_length=20, null=False, unique=True)
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
    email = models.EmailField(blank=True, null=None)
    first_name = models.CharField(max_length=50, default=None)
    last_name = models.CharField(max_length=50, default=None)
    is_active = models.BooleanField(_('active'), default =True)
    program = models.CharField(max_length=50, default='Test')

class InspirationalQuotes(models.Model):
    quote = models.CharField(max_length=500, blank=True, null=True)
    
    def __str__(self):
        return str(self.quote)
    

class Affirmations(models.Model):
    affirmation = models.CharField(max_length=500, blank=True, null=True)
    published_date = models.DateField(null=True, blank=False)

    def __str__(self):
        return str(self.affirmation)

class Dailyquote(models.Model):
    dailyquote = models.CharField(max_length=500, blank=True, null=True)
    quote_date = models.DateField(null=True, blank=False)
    description = models.CharField(max_length=500, blank=True, null=True)
    def __str__(self):
        return str(self.dailyquote)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default='profile_image/default.jpg', upload_to='profile_image', blank=True)
    bio = models.CharField(max_length=255, blank=False, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    secondary_email = models.EmailField(max_length=255, blank=True, null=True)
    other_email = models.EmailField(max_length=255, blank=True, null=True)
    zip = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=25, blank=True, null=True)
    county = models.CharField(max_length=25, blank=True, null=True)
    state = models.CharField(max_length=25, blank=True, null=True)
    country = models.CharField(max_length=25, blank=True, null=True)
    day_phone = models.CharField(blank=True, null=True, max_length=13)
    eve_phone = models.CharField(blank=True, null=True, max_length=13)
    age_group = models.IntegerField(choices=EVENT, blank=False, null=True)
    school = models.CharField(max_length=50, blank=True, null=True)
    points = models.IntegerField(default=0,blank=True, null=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, default=None, blank=True, null=True)
    profile_filled = models.BooleanField(default=False)
    pre_assessment = models.CharField(default='No', blank=True, null=True, max_length=50)
    post_assessment = models.CharField(default='No', blank=True, null=True, max_length=50)


    def __str__(self):
        return f'{self.user.username} Profile'

    @property
    def age(self):
        if self.date_of_birth is None:
            return "None";
        else:
            return int((datetime.now().date() - self.date_of_birth).days / 365.25)


class Inactiveuser(models.Model):
    #inactive_id = models.AutoField(primary_key=True,blank=False,null=False)
    set_days = models.IntegerField(default=7,validators=[MaxValueValidator(31),MinValueValidator(1)])
    #set_days = models.IntegerField(blank=False,null=False,default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    down_at = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return str(self.set_days)

    class Meta:
        get_latest_by = 'created_at'


    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)
    #     instance.profile.save()
    #
    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()
BOOL_CHOICES = [('Yes','yes'),('No','no')]

class Reward(models.Model):
    reward_no = models.AutoField(null=False, primary_key=True)
    user = models.ForeignKey(User, related_name='rewards', on_delete=models.CASCADE)
    points_redeemed = models.IntegerField(blank=True, null=True)
    service_used = models.CharField(max_length=25, blank=True, null=True)
    redeem_status= models.CharField(max_length=10, choices=BOOL_CHOICES, default='No', blank=False, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.reward_no)

    def updated(self):
        self.timestamp = timezone.now()
        self.save()

class RewardsNotification(models.Model):
    #rewards_notification_id = models.AutoField(primary_key=True,blank=False,null=False)
    Rewards_milestone_1 = models.IntegerField(default=25,blank=False,null=False)
    Rewards_milestone_2 = models.IntegerField(default=50, blank=False, null=False)
    Rewards_milestone_3 = models.IntegerField(default=75, blank=False, null=False)
    Rewards_milestone_4 = models.IntegerField(default=100, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.created_at)

    class Meta:
        get_latest_by = 'created_at'


class Testfield(models.Model):
    physical_days_to_done = models.IntegerField(default=1)
    nutrition_days_to_done = models.IntegerField(default=1)
    creation_date = models.DateTimeField(auto_now=True)
    current_values = models.BooleanField(default=True)
    test1 = models.CharField(max_length=25, blank=True, null=True)

class Parameters(models.Model):
    physical_days_to_done = models.IntegerField(default=1)
    nutrition_days_to_done = models.IntegerField(default=1)
    creation_date = models.DateTimeField(auto_now=True)
    current_values = models.BooleanField(default=True)

class Testfield2(models.Model):
    physical_to_done = models.IntegerField(default=1)
    nutrition_days_to_done = models.IntegerField(default=1)
    creation_date = models.DateTimeField(auto_now=True)
    current_values = models.BooleanField(default=True)
    test4 = models.CharField(max_length=25, blank=True, null=True)
