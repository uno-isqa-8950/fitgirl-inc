from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserEditForm, ProgramForm, UploadFileForm, programArchiveForm, EmailForm, CronForm, \
    RewardsNotificationForm, ManagePointForm, ParametersForm, ProgramClone
from .forms import Profile, Program, ContactForm, ProfileEditForm, AdminEditForm, SignUpForm, SchoolsForm
from .forms import RewardItemForm, RewardCategoryForm
from .models import RegisterUser, Dailyquote, Inactiveuser, RewardsNotification, Parameters, Reward, KindnessMessage, \
    CloneProgramInfo, RewardCategory, RewardItem, Schools, Program, Profile, DefaultPassword
from week.models import WeekPage, EmailTemplates, UserActivity, StatementsPage
from week.forms import TemplateForm
from week.models import CustomFormSubmission
from io import StringIO
import re, json
#import weasyprint
from io import BytesIO
from django.shortcuts import redirect
import csv
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from empoweru.settings import CLIENT_EMAIL
import datetime, tzlocal
from django.core.mail import BadHeaderError, send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from wagtail.core.models import Page
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core import serializers, exceptions
# from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import datetime, pytz, re
from account.models import Inactiveuser, CloneProgramInfo, Program
from wagtail.core.models import Page
from week.models import PhysicalPostPage
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
# from datetime import datetime, timedelta
# from datetime import timedelta
from account.todays_date import todays_date
from account.tomorrows_date import tomorrows_date
from week.models import welcomepage
import pandas as pd




@login_required
def cloneprogram(request):
    if request.method == "POST":
        form = ProgramClone(request.POST)
        if form.is_valid():
            user = request.user
            new_start_date = str(form.cleaned_data['new_start_date'])
            program_to_clone = form.cleaned_data['program_to_clone']
            new_program = form.clean()['new_program']

            date_fields = new_start_date.split('-')
            new_start_datetime = datetime.datetime(int(date_fields[0]), int(date_fields[1]), int(date_fields[2]),
                                                   tzinfo=tzlocal.get_localzone())
            new_program_slug = '-'.join(new_program.lower().split(' '))

            if Page.objects.filter(slug=new_program_slug).count() > 0 \
                    or Page.objects.filter(title=new_program).count() > 0:
                message = "Error: A program with this name already exists"
            elif CloneProgramInfo.objects.filter(new_program=new_program, active=True).count() > 0:
                message = "Error: This program is already scheduled for setup"
            else:
                new_program_info = CloneProgramInfo()
                new_program_info.program_to_clone = program_to_clone
                new_program_info.new_program = new_program
                new_program_info.new_start_date = new_start_datetime
                new_program_info.active = True
                new_program_info.user = user
                new_program_info.save()
                message = 'Your program is being created.  This will take several minutes. You will receive an email when the process is complete.'
                return render(request, 'account/cloneprogram.html', {'form': form, 'message': message})
        else:
            message = 'Error: Invalid data'
            return render(request, 'account/cloneprogram.html', {'form': form, 'message': message})
    else:
        form = ProgramClone()
        return render(request, 'account/cloneprogram.html', {'form': form})

