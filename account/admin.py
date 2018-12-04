# from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Program
from .models import Profile, RegisterUser, Affirmation, InspirationalQuote
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
#admin.site.register(Profile)
admin.site.register(RegisterUser)

class AffirmationAdmin(admin.ModelAdmin):
    Quotes = 'Quotes'
admin.site.register(Affirmation, AffirmationAdmin)


class InspirationalAdmin(admin.ModelAdmin):
    InspirationalQuote = 'Inspirational Quotes'
admin.site.register(InspirationalQuote, InspirationalAdmin)


