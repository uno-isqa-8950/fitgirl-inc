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
    (3, _("14-16")),

)

BACKGROUND_CHOICES = [
    ('pink', 'Pink'),
    ('blue', 'Blue'),
    ('yellow', 'Yellow'),
    ('green', 'Green'),
    ('orange', 'Orange'),
]


class KindnessCardTemplate(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False, default=1)
    image_name = models.CharField(max_length=25, null=True, blank=True, default='../account/static/images/KCard.jpg')
    image = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return str(self.image_name)


class Program(models.Model):
    # program_id = models.AutoField(null=False, primary_key=True)
    program_name = models.CharField(max_length=20, null=False, unique=True)
    program_start_date = models.DateField(null=False, blank=False)
    program_end_date = models.DateField(null=False, blank=False)
    KCardTemplate = models.ForeignKey(KindnessCardTemplate, on_delete=models.CASCADE, null=True, blank=True, default=1)
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
    email = models.EmailField(blank=True, null=None, unique=True)
    first_name = models.CharField(max_length=50, default=None)
    last_name = models.CharField(max_length=50, default=None)
    is_active = models.BooleanField(_('active'), default=True)
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
    age_group = models.IntegerField(choices=EVENT, blank=False, null=True, default=1)
    school = models.CharField(max_length=50, blank=True, null=True)
    points = models.IntegerField(default=0, blank=True, null=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, default=None, blank=True, null=True)
    select_your_background_color_for_website = models.CharField(max_length=50, choices=BACKGROUND_CHOICES, blank=False,
                                                                null=True, default='pink')
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
    inactive_id = models.AutoField(primary_key=True, blank=False, null=False)
    set_days = models.IntegerField(default=7, validators=[MaxValueValidator(31), MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    down_at = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return str(self.set_days)

    class Meta:
        get_latest_by = 'created_at'


BOOL_CHOICES = [('Yes', 'yes'), ('No', 'no')]


class Reward(models.Model):
    reward_no = models.AutoField(null=False, primary_key=True)
    user = models.ForeignKey(User, related_name='rewards', on_delete=models.CASCADE)
    points_redeemed = models.IntegerField(blank=True, null=True)
    service_used = models.CharField(max_length=25, blank=True, null=True)
    redeem_status = models.CharField(max_length=10, choices=BOOL_CHOICES, default='No', blank=False, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.reward_no)

    def updated(self):
        self.timestamp = timezone.now()
        self.save()


class RewardsNotification(models.Model):
    rewards_notification_id = models.AutoField(primary_key=True, blank=False, null=False)
    Rewards_milestone_1 = models.IntegerField(default=25, blank=False, null=False)
    Rewards_milestone_2 = models.IntegerField(default=50, blank=False, null=False)
    Rewards_milestone_3 = models.IntegerField(default=75, blank=False, null=False)
    Rewards_milestone_4 = models.IntegerField(default=100, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.rewards_notification_id)

    class Meta:
        get_latest_by = 'created_at'


class Parameters(models.Model):
    physical_days_to_done = models.IntegerField(default=1)
    nutrition_days_to_done = models.IntegerField(default=1)
    rewards_active = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now=True)
    current_values = models.BooleanField(default=True)

class KindnessMessage(models.Model):
    message_program = models.CharField(max_length=20, blank=True, null=True)  # sdizdarevic added for archiving messages from previous programs 3/11/2020
    user = models.ForeignKey(User, null=True, blank=False, on_delete=models.CASCADE)  #sdizdarevic added so that kindness messages are delted when users are deleted 3/11/2020
    message_id = models.AutoField(null=False, primary_key=True)
   # user = models.ForeignKey(User, related_name='all_messages', on_delete=models.CASCADE)
   # user = models.ForeignKey(User, related_name='message_id', on_delete=models.CASCADE)
    body = models.CharField(max_length=500, blank=True, null=True)
    from_user = models.CharField(max_length=50, blank=False, null=False)
    to_user = models.CharField(max_length=50, blank=False, null=False)
    read_message = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.body)

    def __str__(self):
        return str(self.user_id)
        self.save()


class RewardCategory(models.Model):
    category = models.CharField(max_length=25, blank=False, null=False, unique=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    category_image = models.ImageField(blank=True, default='reward_categories/default.jpg',
                                       upload_to='reward_categories/')

    def __str__(self):
        return str(self.category)


class RewardItem(models.Model):
    item = models.CharField(max_length=25, blank=False, null=False, unique=True)
    description = models.CharField(max_length=50, blank=False, null=False)
    category = models.ForeignKey(RewardCategory, on_delete=models.SET_NULL, blank=True, null=True)
    points_needed = models.IntegerField(default=25)
    qty_available = models.IntegerField(default=1)
    reward_image = models.ImageField(blank=True, upload_to='reward_items/')

    def __str__(self):
        return str(self.item)


class CloneProgramInfo(models.Model):
    program_to_clone = models.CharField(max_length=25, blank=False, null=False)
    new_start_date = models.DateField(blank=False, null=False)
    new_program = models.CharField(max_length=25, null=False, blank=False)
    user = models.ForeignKey(User, blank=False, null=True, on_delete=models.SET_NULL)
    active = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.new_program)


class Schools(models.Model):
    schools_id = models.AutoField(primary_key=True, blank=False, null=False)
    schools_name = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return str(self.schools_name)

