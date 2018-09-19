# from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Program

# Register your models here.

class ProgramList(admin.ModelAdmin):
    list_display = ('program_name', 'program_start_date', 'program_end_date')
    list_filter = ('program_name', 'program_start_date')
    search_fields = ('program_name', 'program_start_date')
    ordering = ['program_name']


admin.site.register(Program, ProgramList)

