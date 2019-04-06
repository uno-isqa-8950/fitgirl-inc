# from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Program
from .models import Profile, RegisterUser, InspirationalQuotes, Dailyquote,Inactiveuser,RewardsNotification, Affirmations, Reward, KindnessMessage, RewardCategory, RewardItem,School
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

# Register your models here.

class ProgramList(admin.ModelAdmin):
    list_display = ('program_name', 'program_start_date', 'program_end_date')
    list_filter = ('program_name', 'program_start_date')
    search_fields = ('program_name', 'program_start_date')
    ordering = ['program_name']


admin.site.register(Program, ProgramList)

# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ['user','first_name','last_name','bio','date_of_birth', 'photo']

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
#admin.site.register(Inactiveuser)
#admin.site.register(Profile)
admin.site.register(RegisterUser)


# class AffirmationAdmin(admin.ModelAdmin):
#     Quotes = 'Quotes'
#     list_display = ('affirmation', 'published_date')
#     list_filter = ('affirmation', 'published_date')
#     search_fields = ('affirmation', 'published_date')
#
# admin.site.register(Affirmations, AffirmationAdmin)

class DailyquoteAdmin(admin.ModelAdmin):
    list_display = ('dailyquote', 'quote_date')
    list_filter = ('dailyquote', 'quote_date')
    search_fields = ('dailyquote', 'quote_date')

admin.site.register(Dailyquote, DailyquoteAdmin)

class InspirationalAdmin(admin.ModelAdmin):
    InspirationalQuote = 'Inspirational Quotes'
admin.site.register(InspirationalQuotes, InspirationalAdmin)


class InactiveusersAdmin(admin.ModelAdmin):
    Inactiveuser = 'Inactiveuser'
    list_display = ('set_days','created_at','updated_at')

admin.site.register(Inactiveuser,InactiveusersAdmin)


class RewardsNotificationAdmin(admin.ModelAdmin):
    list_display = ('Rewards_milestone_1','Rewards_milestone_2','Rewards_milestone_3','Rewards_milestone_4')

admin.site.register(RewardsNotification,RewardsNotificationAdmin)

class RewardList(admin.ModelAdmin):
    list_display = ('reward_no', 'user', 'timestamp')
    list_filter = ('user', 'timestamp')
    search_fields = ('user', 'timestamp')
    ordering = ['timestamp']

admin.site.register(Reward, RewardList)

class RewardCategories(admin.ModelAdmin):
    list_display = ('category', 'description')
    list_filter = ('category', 'description')
    search_fields = ['category']
    ordering = ['category']

admin.site.register(RewardCategory, RewardCategories)

class RewardItems(admin.ModelAdmin):
    list_display = ('item', 'description', 'category', 'points_needed', 'qty_available')
    list_filter = ('item', 'category')
    search_fields = ('item', 'qty_available')
    ordering = ['category']

admin.site.register(RewardItem, RewardItems)

class KindnessMessageAdmin(admin.ModelAdmin):
    list_display = ('message_id','from_user', 'to_user', 'body', 'created_date')
    list_filter = ('from_user', 'to_user', 'created_date')
    search_fields = ('from_user', 'to_user')
    ordering = ['created_date']

admin.site.register(KindnessMessage, KindnessMessageAdmin)

class SchoolAdmin(admin.ModelAdmin):
    School = 'School'
    list_display = ('school_name',)

admin.site.register(School,SchoolAdmin)