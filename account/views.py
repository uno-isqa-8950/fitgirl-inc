from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserEditForm, ProfileEditForm, ProgramForm, UploadFileForm, programArchiveForm, EmailForm,CronForm,RewardsNotificationForm,ManagePointForm, ParametersForm, ProgramClone
from .forms import Profile,User, Program, ContactForm, ProfileEditForm, AdminEditForm, SignUpForm,SchoolForm
from .forms import RewardItemForm, RewardCategoryForm
from .models import RegisterUser, Affirmations, Dailyquote, Inactiveuser, RewardsNotification, Parameters, Reward, KindnessMessage, CloneProgramInfo, RewardCategory, RewardItem,School
from week.models import WeekPage, EmailTemplates, UserActivity, ServicePostPage, KindnessCardPage
from week.forms import TemplateForm
from week.models import CustomFormSubmission, PhysicalPostPage
from io import TextIOWrapper, StringIO
import re, json
import weasyprint
from io import BytesIO
from django.shortcuts import redirect
import csv, string, random
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.forms import ValidationError
#from datetime import datetime, timedelta
import pytz, datetime, tzlocal
import wagtail
from django.core.mail import send_mass_mail, BadHeaderError, send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from wagtail.core.models import Page
from django.db.models.signals import post_save, post_init, pre_save
from django.dispatch import receiver
from django.core import serializers
from collections import defaultdict

@receiver(post_save, sender=Profile)
def point_check(sender, instance, **kwargs):
    try:
        milestones = RewardsNotification.objects.latest()
        obj = Profile.objects.get(pk=instance.pk)
        set_point1 = milestones.Rewards_milestone_1
        set_point2 = milestones.Rewards_milestone_2
        set_point3 = milestones.Rewards_milestone_3
        set_point4 = milestones.Rewards_milestone_4
    except RewardsNotification.DoesNotExist:
        obj = Profile.objects.get(pk=instance.pk)
        set_point1 = 25
        set_point2 = 50
        set_point3 = 75
        set_point4 = 100
    if obj.user.profile.points == set_point1 or obj.user.profile.points == set_point2 or obj.user.profile.points == set_point3 or obj.user.profile.points == set_point4:
        rewards_notification = "True"
        messages = EmailTemplates.objects.get()
        subject = messages.subject_for_rewards_notification + ' :' + str(obj.user.profile.points)
        html_message = render_to_string('account/group_email_template.html',
                                        {'content': messages, 'rewards_notification': rewards_notification})
        plain_message = strip_tags(html_message)
        from_email = 'capstone18FA@gmail.com'
        send_mail(subject, plain_message, from_email, [obj.user.email], html_message=html_message)
    else:
        pass

'''
@receiver(post_save, sender=KindnessMessage)
def unread_message_check(sender, instance, **kwargs):
    obj = KindnessMessage.objects.get(pk=instance.pk)
    if obj.read_messages == False:
        obj.read_messages.count()
'''

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    today = datetime.date.today()
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)

    dailyquote = Dailyquote.objects.filter(quote_date__gte=today).filter(quote_date__lt=tomorrow)

    programs = Program.objects.filter(program_start_date__lt=today).filter(program_end_date__gte=today)
    for program in programs:
        current_program = program.program_name
        current_program_lower = current_program.lower()
        gap_pos = current_program_lower.find(" ")
        new_str = current_program_lower[0:gap_pos] + '-' + current_program_lower[gap_pos:]
        new_str1 = new_str.replace(" ", "")

    weeks = WeekPage.objects.filter(end_date__gte=today, start_date__lte=today)
    for this_week in weeks:
        print(this_week.title)
        todays_week = this_week.title.lower()
        print(todays_week)
        week_gap_pos = todays_week.find(" ")
        new_week_str = todays_week[0:week_gap_pos] + '-' + todays_week[week_gap_pos:]
        print(new_week_str)
        new_week_str1 = new_week_str.replace(" ", "")

    if request.user.is_staff:
        registeredUsers = User.objects.filter(is_superuser=False).order_by('-is_active')
        return render(request, 'account/viewUsers.html', {'registeredUsers': registeredUsers})

    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard', 'dailyquote': dailyquote, 'new_str1': new_str1,
                   'new_week_str1': new_week_str1})


@login_required
def login_success(request):
    today = datetime.date.today()
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    dailyquote = Dailyquote.objects.filter(quote_date__gte=today).filter(quote_date__lt=tomorrow)
    if request.user.is_staff:
        registeredUsers = User.objects.filter(is_superuser=False).order_by('-is_active')
        return render(request, 'account/viewUsers.html', {'registeredUsers': registeredUsers})
    elif request.user.is_active:
        current_week = WeekPage.objects.live().filter(end_date__gte=today, start_date__lte=today)
        print(current_week)
        return render(request,
                      'account/current_week.html',
                      {'current_week': current_week,
                       'dailyquote': dailyquote})

@login_required
def userdashboard(request):
    return render(request,
                  'account/userdashboard.html',
                  {'section': 'userdashboard'})

@login_required
def createprogram(request):
    registeredPrograms = Program.objects.all()
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            #print ("program_form")
            program= form.save(commit=False)
            #program.created_date = timezone.now()
            program.save()
            messages.success(request,'Program added successfully')
            return redirect('createprogram')
        else:
            messages.error(request, 'Error creating Program. Retry!')
            #return HttpResponse('Error updating your profile!')
    else:
        form = ProgramForm()
        #print("Else")
        #profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/createprogram.html',
                  {'section': 'createprogram','form':form,'registeredPrograms':registeredPrograms})


# def validate_csv(value):
#     if not value.name.endswith('.csv'):
#         raise ValidationError('Invalid file type')

def handle_uploaded_file(request, name):
    csvf = StringIO(request.FILES['file'].read().decode())
    reader = csv.reader(csvf, delimiter=',')
    reader.__next__();
    count = 0
    failcount = 0
    existcount = 0
    emailcount = 0
    for row in reader:
        try:
            if row[1] and row[2] and row[3]:
                if re.match(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', row[1]):
                    num = len(User.objects.all().filter(email=row[1]))
                    if (len(User.objects.all().filter(email=row[1])) > 0):
                        # targetUser = User.objects.all().filter(email=row[1])[0]
                        # targetUser.is_active = True
                        # targetUser.save()
                        # targetProfile = targetUser.profile
                        # targetProfile.program = Program.objects.all().filter(program_name=name)[0]
                        # targetProfile.points = 0
                        # targetProfile.pre_assessment = 'No'
                        # targetProfile.post_assessment = 'No'
                        # targetProfile.save()
                        existcount += 1             #hghanta: changes to get existing users count

                    else:
                        vu = RegisterUser(email=row[1], first_name=row[2], last_name=row[3], program=name)
                        current_site = get_current_site(request)
                        alphabet = string.ascii_letters + string.digits
                        # theUser = User(username=generate(), password = generate_temp_password(8), first_name = row[2],last_name = row[3], email =row[1])
                        theUser = User(username=vu.email, first_name=row[2], last_name=row[3], email=row[1])
                        theUser.set_password('stayfit2019')
                        theUser.save()
                        profile = Profile.objects.create(user=theUser,
                                                         program=Program.objects.all().filter(program_name=name)[0])
                        profile.save()
                        form = PasswordResetForm({'email': theUser.email})
                        if form.is_valid():
                            request = HttpRequest()
                            request.META['SERVER_NAME'] = 'www.empoweruomaha.com'
                            request.META['SERVER_PORT'] = '80'
                            form.save(
                                request=request,
                                from_email=settings.EMAIL_HOST_USER,
                                subject_template_name='registration/new_user_subject.txt',
                                email_template_name='registration/password_reset_newuser_email.html')
                        if vu is not None:
                            vu.save()
                            count = count + 1
                else:
                    emailcount += 1
            else:
                failcount += 1
        except Exception as e:
            print(e)
            existcount += 1
    return (count, failcount, existcount, emailcount)


def get_short_name(self):
    # The user is identified by their email address
    return self.first_name


@login_required
def registerusers(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_name = request.FILES['file']
            if not file_name.name.endswith('.csv'):
                messages.info(request, f'You need to upload a CSV file.')
                return redirect('registerusers')

            else:
                value,fail,existing,bademail = handle_uploaded_file(request,form.cleaned_data['programs'])

                if value==0 and fail==0 and existing==0 and bademail==0:
                    form = request.POST
                    messages.error(request, 'Your upload file is empty.Try again!')
                    return redirect('registerusers')
                elif value==0 and fail==0 and existing==0 and bademail>0:
                    form = request.POST
                    messages.info(request, f'Number of invalid email address: {bademail}')
                    return redirect('registerusers')
                elif value==0 and fail==0 and existing>0 and bademail==0:
                    form = request.POST
                    messages.info(request, f'Number of user-account already exist: {existing}')
                    return redirect('registerusers')
                elif value==0 and fail==0 and existing>0 and bademail>0:
                    form = request.POST
                    messages.info(request, f'Number of user-account already exist: {existing}')
                    messages.info(request, f'Number of invalid email address: {bademail}')
                    return redirect('registerusers')
                elif value==0 and fail>0 and existing==0 and bademail==0:
                    form = request.POST
                    messages.info(request, f'Number of user-account not added: {fail}')
                    return redirect('registerusers')
                elif value==0 and fail>0 and existing==0 and bademail>0:
                    form = request.POST
                    messages.info(request, f'Number of user-account not added: {fail}')
                    messages.info(request, f'Number of invalid email address: {bademail}')
                    return redirect('registerusers')
                elif value==0 and fail>0 and existing>0 and bademail==0:
                    form = request.POST
                    messages.info(request, f'Number of user-account not added: {fail}')
                    messages.info(request, f'Number of user-account already exist: {existing}')
                    return redirect('registerusers')
                elif value==0 and fail>0 and existing>0 and bademail>0:
                    form = request.POST
                    messages.info(request, f'Number of user-account not added: {fail}')
                    messages.info(request, f'Number of user-account already exist: {existing}')
                    messages.info(request, f'Number of invalid email address: {bademail}')
                    return redirect('registerusers')

                elif value>0 and fail==0 and existing==0 and bademail>0:
                    form = request.POST
                    messages.info(request, f'Number of user-account added successfully: {value}')
                    messages.info(request, f'Number of invalid email address: {bademail}')
                    return redirect('registerusers')
                elif value>0 and fail==0 and existing>0 and bademail==0:
                    form = request.POST
                    messages.info(request, f'Number of user-account added successfully: {value}')
                    messages.info(request, f'Number of user-account already exist: {existing}')
                    return redirect('registerusers')
                elif value>0 and fail==0 and existing>0 and bademail>0:
                    form = request.POST
                    messages.info(request, f'Number of user-account added successfully: {value}')
                    messages.info(request, f'Number of user-account already exist: {existing}')
                    messages.info(request, f'Number of invalid email address: {bademail}')
                    return redirect('registerusers')
                elif value>0 and fail>0 and existing==0 and bademail==0:
                    form = request.POST
                    messages.info(request, f'Number of user-account added successfully: {value}')
                    messages.info(request, f'Number of user-account already exist: {fail}')
                    return redirect('registerusers')
                elif value>0 and fail>0 and existing==0 and bademail>0:
                    form = request.POST
                    messages.info(request, f'Number of user-account added successfully: {value}')
                    messages.info(request, f'Number of user-account not added: {fail}')
                    messages.info(request, f'Number of invalid email address: {bademail}')
                    return redirect('registerusers')
                elif value>0 and fail>0 and existing>0 and bademail==0:
                    form = request.POST
                    messages.info(request, f'Number of user-account added successfully: {value}')
                    messages.info(request, f'Number of user-account not added: {fail}')
                    messages.info(request, f'Number of user-account already exist: {existing}')
                    return redirect('registerusers')
                elif value>0 and fail>0 and existing>0 and bademail>0:
                    form = request.POST
                    messages.info(request, f'Number of user-account added successfully: {value}')
                    messages.info(request, f'Number of user-account not added: {fail}')
                    messages.info(request, f'Number of user-account already exist: {existing}')
                    messages.info(request, f'Number of invalid email address: {bademail}')
                    return redirect('registerusers')
                else:
                    form = request.POST
                    messages.success(request, f'Number of user-account added successfully: {value}')
                    return redirect('users')
    else:
        form = UploadFileForm()
    return render(request,
                  'account/registerusers.html',
                  {'form' : form})

def aboutus(request):
    return render(request,
                  'account/aboutus.html',
                  {'section': 'aboutus'})

@login_required
def users(request):
    registeredUsers = User.objects.filter(is_superuser = False)
    return render(request, 'account/viewUsers.html', {'registeredUsers' : registeredUsers})

@login_required
def myprogram(request):
    return render(request,
                  'account/myprogram.html',
                  {'section': 'myprogram'})
@login_required
def programs(request):
    return render(request,
                  'account/programs.html',
                  {'section': 'programs'})
@login_required
def edit(request):

    activated = False
    print(request.user.profile.profile_filled)
    if(request.user.profile.profile_filled):
        activated = True
    else:
        activated = False


    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            theProfile = request.user.profile
            theProfile.profile_filled = True
            theProfile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('/pages/pre-assessment/')
        else:
            messages.warning(request, 'Please correct the errors below!')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'activated':activated})

@login_required
def user_edit(request):

    activated = False
    print(request.user.profile.profile_filled)
    if(request.user.profile.profile_filled):
        activated = True
    else:
        activated = False


    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            theProfile = request.user.profile
            theProfile.profile_filled = True
            theProfile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('/pages/userdashboard')
        else:
            messages.warning(request, 'Please correct the errors below!')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/user_edit_profile.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'activated':activated})


@login_required
def admin_edit(request):
    if request.method == 'POST':
        # update
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        admin_form = AdminEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and admin_form.is_valid():
            user_form.save()
            admin_form.save()
            theProfile = request.user.profile
            theProfile.profile_filled = True
            theProfile.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('users')
        else:
            messages.warning(request, 'Please correct the errors below!')
    else:
        # edit
        user_form = UserEditForm(instance=request.user)
        admin_form = AdminEditForm(instance=request.user.profile)

    return render(request, 'account/admin_edit.html', {'user_form': user_form, 'admin_form': admin_form})



@login_required
def profile(request,pk):
    pro = Profile.objects.get(user_id=pk)
    return render(request,
                  'account/profile.html',
                  {'user': pro})

@login_required
def cms_frame(request):
    return render(request,
                  'account/cms_frame.html',
                  {'section': 'cms_frame'})
@login_required
def django_frame(request):
    return render(request,
                  'account/django_frame.html',
                  {'section': 'django_frame'})

@login_required
def archive(request):
    if request.method == 'POST':
        form = programArchiveForm(request.POST)
        if form.is_valid():
            theProgram =  Program.objects.all().filter(program_name = form.cleaned_data['programs'])[0]
            profiles =Profile.objects.all().filter(program = theProgram)
            for theProfile in profiles:
                if(theProfile.user.is_superuser == False):
                    theUser = theProfile.user
                    theUser.is_active = False
                    theUser.save()
            messages.success(request, 'Users archived successfully')
            return redirect('archive')
        else:
                    messages.error(request, 'Error archiving users. Retry!')
                    #messages.success(request, 'Users archived successfully')
    else:
        form = programArchiveForm()
    return render(request,
                  'account/archive.html',
                  {'section': 'archive','form':form})


def group_email(request):
    if request.method == 'GET':
        form = EmailForm()
        return render(request, "account/group_email.html", {'form': form})
    else:
        form = EmailForm()
        template_form = TemplateForm()
        list = request.POST.getlist('checks[]')
        return render(request, "account/group_email.html", {'form': form, 'template_form': template_form, 'to_list': list})




def send_group_email(request):
    if request.method == 'GET':
        return render(request, "account/group_email.html")
    else:
        template_form = TemplateForm(request.POST)
        form = EmailForm(request.POST)
        if form.is_valid() :
            selection = request.POST.get('selection')
            list = request.POST.get('to_list')
            new = list.replace('[','').replace(']','').replace("'",'')
            result = [x.strip() for x in new.split(',')]
            from_email = 'capstone18FA@gmail.com'
            subject = form.cleaned_data['subject']
            name_list = []
            if selection == 'text':
                message = form.cleaned_data['message']
                for user_email in result:
                    send_mail(subject, message, from_email, [user_email])
                    user = User.objects.get(username = user_email)
                    name = user.first_name + " " + user.last_name
                    name_list.append(name)
                return render(request, "account/email_confirmation.html", {'name_list': name_list, 'form': form})
            elif template_form.is_valid() and selection == 'CMS content':
                template = request.POST.get('templates')
                field = template.replace('week.EmailTemplates.', '')
                content = EmailTemplates.objects.get()
                group_message = 'False'
                user_inactivity = 'False'
                rewards_notification = 'False'
                if field == 'group_message':
                    group_message = 'True'
                    subject = content.subject_for_group
                elif field == 'inactivity_message':
                    user_inactivity = 'True'
                    subject = content.subject_for_inactivity
                elif field == 'rewards_message':
                    rewards_notification = 'True'
                    subject = content.subject_for_rewards_notification
                html_message = render_to_string('account/group_email_template.html', {'content': content,
                                                                                      'group_message': group_message,
                                                                                      'user_inactivity': user_inactivity,
                                                                                      'rewards_notification': rewards_notification})
                plain_message = strip_tags(html_message)
                for user_email in result:
                    send_mail(subject, plain_message, from_email, [user_email], html_message=html_message)
                    user = User.objects.get(username = user_email)
                    name = user.first_name + " " + user.last_name
                    name_list.append(name)
                return render(request, "account/email_confirmation.html", {'name_list': name_list, 'form': form})



def email_individual(request,pk):
    user_student = get_object_or_404(User,pk=pk)
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            #contact_email = form.cleaned_data['contact_email']
            contact_email = user_student.email
            message = form.cleaned_data['message']
            from_email = 'capstone18FA@gmail.com'

            try:
                send_mail(subject, message, from_email, [contact_email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return render(request,'account/email_individual_confirmation.html',{'contact_email': contact_email},{'user_student':user_student})
    return render(request, 'account/email_individual.html', {'form': form,'user_student':user_student})



@login_required
def user_inactivity(request):
    try:
        user_inactive_days = Inactiveuser.objects.latest()
        latest_date = user_inactive_days.set_days
    except Inactiveuser.DoesNotExist:
        latest_date = 7

    if request.method == 'GET':
        form = CronForm(initial={'days':latest_date})
    else:
        form = CronForm(request.POST,initial={'days':latest_date})
        if form.is_valid():
            inactive_days = form.cleaned_data['days']
            days_data = Inactiveuser(set_days=inactive_days)
            days_data.save()
            messages.success(request,'User inactivity email notification period set successfully')
            return redirect('user_inactivity')
    return render(request,'account/user_inactivity.html',{'form':form})


def rewards_notification(request):
    try:
        milestones = RewardsNotification.objects.latest()
        set_point1 = milestones.Rewards_milestone_1
        set_point2 = milestones.Rewards_milestone_2
        set_point3 = milestones.Rewards_milestone_3
        set_point4 = milestones.Rewards_milestone_4
    except RewardsNotification.DoesNotExist:
        set_point1 = 25
        set_point2 = 50
        set_point3 = 75
        set_point4 = 100

    if request.method == 'GET':
        form = RewardsNotificationForm(initial={'Rewards_milestone_1':set_point1,'Rewards_milestone_2':set_point2,'Rewards_milestone_3':set_point3,'Rewards_milestone_4':set_point4})
    else:
        form = RewardsNotificationForm(request.POST,initial={'Rewards_milestone_1':set_point1,'Rewards_milestone_2':set_point2,'Rewards_milestone_3':set_point3,'Rewards_milestone_4':set_point4})
        if form.is_valid():
            Rewards_milestone_1 = form.cleaned_data['Rewards_milestone_1']
            Rewards_milestone_2 = form.cleaned_data['Rewards_milestone_2']
            Rewards_milestone_3 = form.cleaned_data['Rewards_milestone_3']
            Rewards_milestone_4 = form.cleaned_data['Rewards_milestone_4']
            rewards_notification_data = RewardsNotification(Rewards_milestone_1=Rewards_milestone_1,Rewards_milestone_2=Rewards_milestone_2,Rewards_milestone_3=Rewards_milestone_3,Rewards_milestone_4=Rewards_milestone_4)
            rewards_notification_data.save()
            messages.success(request,'Rewards email notification milestones set successfully')
            return render(request,'account/rewards_notification.html',{'form':form})
    return render(request,'account/rewards_notification.html',{'form':form})

def manage_points(request):
    if request.method == 'GET':
        form = ManagePointForm()
        return render(request, "account/managepoints.html", {'form': form})
    else:
        form = ManagePointForm()
        list = request.POST.getlist('checks[]')
        users = []
        for email in list:
            user1 = User.objects.get(username=email)
            users.append(user1)
        return render(request, "account/managepoints.html", {'form': form, 'users': users, 'to_list': list})

def update_points(request):
    if request.method == 'GET':
        form = ManagePointForm()
        return render(request, "account/managepoints.html", {'form': form})
    else:
        form = ManagePointForm(request.POST)
        if form.is_valid():
            list = request.POST.get('to_list')
            new = list.replace('[','').replace(']','').replace("'",'')
            result = [x.strip() for x in new.split(',')]
            manage_points = form.cleaned_data['manage_points']
            added_points = int(manage_points)
            users = []
            for user_email in result:
                user = User.objects.get(username=user_email)
                users.append(user.email)
                point = user.profile.points
                point += added_points
                user.profile.points = point
                user.profile.save()
            messages.success(request, f'{added_points} points has been updated to {users}')
            return redirect('users')


def parameters_form(request):
    if request.method == "POST":
        form = ParametersForm(request.POST)
        if form.is_valid():
            rows = Parameters.objects.filter(current_values=True)
            rows.update(current_values=False)
            post = form.save(commit=False)
            post.save()
    else:
        # Check if Parameters is populated. If not, add default row.
        if Parameters.objects.filter(current_values=True).count() == 0:
            parameters = Parameters()
            parameters.physical_days_to_done = 1
            parameters.nutrition_days_to_done = 1
            parameters.current_values = True
            parameters.save()
        settings = Parameters.objects.get(current_values=True)
        pdtd = settings.physical_days_to_done
        ndtd = settings.nutrition_days_to_done

        form = ParametersForm(
            initial={'physical_days_to_done': pdtd,
                     'nutrition_days_to_done': ndtd}
        )
    return render(request, 'account/parameters_edit.html', {'form': form})

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
            new_start_datetime = datetime.datetime(int(date_fields[0]), int(date_fields[1]), int(date_fields[2]), tzinfo=tzlocal.get_localzone())
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

@login_required
def analytics(request):
    return render(request, 'account/analytics_home.html', {})

@login_required
def export_data(request):
    if request.method == 'POST':

        response = HttpResponse(content_type='text/csv')
        post_data = request.POST
        export_type = post_data['export_type']

        if export_type == 'useractivity':
            response['Content-Disposition'] = 'attachment; filename="useractivity.csv"'
            rows = list(UserActivity.objects.all())
            writer = csv.writer(response)

            writer.writerow(['User', 'Program', 'Activity',
                               'Week Number', 'Day of Week',
                               'Points Earned', 'Date'])
            for row in rows:
                user = User.objects.get(id=row.user_id)
                name = user.first_name + " " + user.last_name
                try:
                    program = Program.objects.get(id=row.program_id).program_name
                except AttributeError:
                    program = ""

                writer_row = [name, program,
                              row.Activity, row.Week,
                              row.DayOfWeek, row.points_earned,
                              row.creation_date]
                writer.writerow(writer_row)

        elif export_type == 'preassessment':
            response['Content-Disposition'] = 'attachment; filename="pre-assessment.csv"'
            try:
                assesssment_page_id = Page.objects.filter(slug__contains="pre-assessment").first().id
                rows = list(CustomFormSubmission.objects.filter(page_id=assesssment_page_id))
            except AttributeError:
                rows = list()

            if len(rows) > 0:
                writer = csv.writer(response)
                header_data = ['User']
                #writer.writerow(['User', 'Pre-assessment Data', 'Submission Time'])

                for row in rows:
                    question_data = json.loads(row.form_data)
                    for key in question_data:
                        header_data.append(str(key))

                header_data.append('Submission Time')
                writer.writerow(header_data)

                for row in rows:
                    row_data = list()
                    user = User.objects.get(id=row.user_id)
                    name = user.first_name + " " + user.last_name
                    row_data.append(name)
                    question_data = json.loads(row.form_data)
                    for key in question_data:
                        row_data.append(str(question_data[key]))
                    row_data.append(row.submit_time.date())
                    writer.writerow(row_data)
            else:
                response = HttpResponse(content_type='text/html', content="No data")
        elif export_type == 'postassessment':
            response['Content-Disposition'] = 'attachment; filename="post-assessment.csv"'
            try:
                assesssment_page_id = Page.objects.filter(slug__contains="post-assessment").first().id
                rows = list(CustomFormSubmission.objects.filter(page_id=assesssment_page_id))
            except AttributeError:
                rows = list()

            if len(rows) > 0:
                writer = csv.writer(response)
                header_data = ['User']
                # writer.writerow(['User', 'Pre-assessment Data', 'Submission Time'])

                for row in rows:
                    question_data = json.loads(row.form_data)
                    for key in question_data:
                        header_data.append(str(key))

                header_data.append('Submission Time')
                writer.writerow(header_data)

                for row in rows:
                    row_data = list()
                    user = User.objects.get(id=row.user_id)
                    name = user.first_name + " " + user.last_name
                    row_data.append(name)
                    question_data = json.loads(row.form_data)
                    for key in question_data:
                        row_data.append(str(question_data[key]))
                    row_data.append(row.submit_time.date())
                    writer.writerow(row_data)
            else:
                response = HttpResponse(content_type='text/html', content="No data")
        else:
            response = HttpResponse(content_type='text/html', content="Invalid Request")
        return response
    else:
        return HttpResponse('Invalid request')

@login_required
def rewards_redeem(request, pk):
    if request.method == "GET":
        #data = ServicePostPage.objects.get(page_ptr_id=10)
        return render(request, 'rewards/reward_confirmation.html')
    else:
        item = RewardItem.objects.get(id=pk)
        points = item.points_needed
        service = item.item
        point = int(points)
        item.qty_available -= 1
        item.save()
        user1 = User.objects.get(username=request.user.username)
        if user1.profile.points < point:
            print('cannot redeem')
        else:
            user1.profile.points = 0
            user1.profile.save()
            points_available = user1.profile.points
            rewards = Reward.objects.create(user=user1, points_redeemed=points, service_used=service)
            reward_number = rewards.reward_no
            subject = 'Confirmation Rewards Redeemed - Redemption No.'.format(rewards.reward_no)
            messages = 'Check the PDF attachment for your redemption number'
            from_email = 'capstone18FA@gmail.com'
            email = EmailMessage(subject, messages, from_email, [user1.email])
            #genarate PDF
            html = render_to_string('rewards/pdf.html',{'point': point, 'service': service,
                                                                        'points_available': points_available,
                                                                        'reward_number': reward_number})
            out = BytesIO()
            stylesheets = [weasyprint.CSS('https://fitgirl-empoweru-prod.s3.amazonaws.com/static/css/pdf.css')]
            weasyprint.HTML(string=html).write_pdf(out,stylesheets=stylesheets)
            email.attach('Redemption No. {}'.format(rewards.reward_no), out.getvalue(), 'application/pdf')
            email.send()
            return render(request, 'rewards/reward_confirmation.html', {'point': point, 'service': service,
                                                                        'points_available': points_available,
                                                                        'reward_number': reward_number})

@login_required
def viewRewards(request):
    rewards = Reward.objects.all()
    user = User.objects.get(username=request.user.username)
    return render(request, 'rewards/viewRewards.html', {'rewards' : rewards, 'user': user})


@login_required
def Analytics_Dashboard(request):
    data = UserActivity.objects.all()
    jsondata = serializers.serialize('json', data, fields=('program', 'user', 'activity', 'week', 'day', 'points_earned'))
    return render(request,
                  'account/Analytics_Dashboard.html',
                  {'section': 'Analytics_Dashboard', 'jsondata':jsondata})
# analytics dashboard ends- srishty#

def send_message(request):
    if request.method == 'POST':
        message = request.POST.get("message")
        to = request.POST.get("user")
        print(to)
        # to = 'one@gmail.com'
        from_user = request.user.username
        KindnessMessage.objects.create(body=message, from_user=from_user, to_user=to)
        user = User.objects.get(username=to)
        name = user.first_name + user.last_name
        messages.success(request, f'Message sent to: {name}')
    return redirect('pages/kindness-card', {'section': 'send_message'})
    # return render(request, 'week/kindness_card_page.html', {'section': 'send_message', 'page': page})

def inbox(request):
    if request.method == 'GET':
        all_messages = KindnessMessage.objects.filter(to_user=request.user.username)
        unread_messages = all_messages.filter(read_message=False)
        # user = User.objects.get(email=request.user.email)
        # unread_message = KindnessMessage.objects.filter(to_user=user).filter(read_message=False)


        dict_all = {}
        dict_unread = {}
        for message in unread_messages:
            username = User.objects.get(username=message.from_user)
            name = username.first_name + " " + username.last_name
            # message.read_message = True
            message.save()
            try:
                dict_unread[name].append(message.body)
            except KeyError:
                dict_unread[name] = [message.body]
        for message in all_messages:
            username = User.objects.get(username=message.from_user)
            name = username.first_name + " " + username.last_name
            # message.read_message = True
            message.save()
            try:
                dict_all[name].append(message.body)
            except KeyError:
                dict_all[name] = [message.body]

        return render(request, 'kindnessCards/new.html', {'messages': messages, 'all': dict_all, 'unread': dict_unread})

def mark_read(request):
    if request.method == 'GET':
        print('inside mark_read')

        all_messages = KindnessMessage.objects.filter(to_user=request.user.username)
        unread_messages = all_messages.filter(read_message=False)
        dict_all = {}
        dict_unread = {}
        for test_message in unread_messages:
            username = User.objects.get(username=test_message.from_user)
            name = username.first_name + " " + username.last_name
            # message.read_message = True
            try:
                dict_unread[name].append(test_message.body)
            except KeyError:
                dict_unread[name] = [test_message.body]
        for message in all_messages:
            username = User.objects.get(username=message.from_user)
            name = username.first_name + " " + username.last_name
            message.read_message = True
            message.save()
            try:
                dict_all[name].append(message.body)
            except KeyError:
                dict_all[name] = [message.body]
        print(dict_unread)
        return redirect('/inbox/')
        # return render(request,
        #               'kindnessCards/new.html',
        #               {'messages': messages, 'all': dict_all, 'unread': dict_unread})

# def inbox_unread(request):
#     if request.method == 'GET':
#         # user = User.objects.get(email=request.user.email)
#         # unread_message = KindnessMessage.objects.filter(to_user=user).filter(read_message=False)
#         # from_users = KindnessMessage.objects.filter(to_user=user).filter(read_message=False).values('from_user')
#         # print(from_users)
#         # print(unread_message)
#         #from_users = KindnessMessage.objects.filter(from_user=)
#         #print(from_users)
#         messages = KindnessMessage.objects.filter(to_user=request.user.email).filter(read_message=False)
#
#         dict = {}
#         photo = 'Photo'
#         for message in messages:
#             username = User.objects.get(username=message.from_user)
#             name = username.first_name + " " + username.last_name
#             picture = username.profile.photo.url
#             #print(username.profile.photo.url)
#             try:
#                 dict[name].append(message.body)
#                 dict['photo'].append(picture)
#             except KeyError:
#                 dict[name] = [message.body]
#                 dict['photo'] = [picture]
#         #print(dict)
#                 #return render(request,'kindnessCards/old.html',{'messages':messages,'inbox':dict,'picture':picture})
#         print(dict)
#         return render(request,'kindnessCards/old.html',{'messages':messages, 'inbox':dict})
#

@login_required()
def edit_user(request,pk):
    user = get_object_or_404(User, pk= pk)
    print(user)
    #user1 = get_object_or_404(Profile, profile.user_id )
    user1 = Profile.objects.filter(user_id=pk).first()


    if request.method == 'POST':
        # update
        form = UserEditForm(instance=user,data=request.POST,files=request.FILES)
        form1 = ProfileEditForm(instance=user1,data=request.POST,files=request.FILES)

        if form1.is_valid() and form.is_valid():
            #user1.profile.photo = ProfileEditForm.cleaned_data['photo']
            user = form.save(commit=False)
            user1 = form1.save(commit=False)
            user1.photo = form1.cleaned_data['photo']
            print(user1.photo)
            user.save()
            user1.save()

            messages.success(request, 'Profile updated successfully')
            return redirect('users')

        else:
            messages.warning(request, 'Please correct the errors below!')
    else:
        # edit
        form = UserEditForm(instance=user)
        form1 = ProfileEditForm(instance=user1)
        return render(request, 'account/edit_user.html', {'form1': form1,'form': form,'user1':user1,'user':user})
    return render(request, 'account/edit_user.html', {'form1': form1,'form': form,'user1':user1,'user':user})


@login_required
def signup(request):
    programs = Program.objects.all()
    if request.method == 'POST':
        sign_form = SignUpForm(data=request.POST)

        if sign_form.is_valid():

            email = sign_form.cleaned_data['email']
            username = email
            first_name = sign_form.cleaned_data['first_name']
            last_name = sign_form.cleaned_data['last_name']
            password = 'stayfit2019'

            selected_program = get_object_or_404(Program, pk=request.POST.get('programs'))

            theUser = User(username= username, email= email, first_name= first_name,
                           last_name=last_name )
            theUser.set_password('stayfit2019')
            theUser.save()

            profile = Profile.objects.create(user=theUser,
                                             program=selected_program)
            profile.save()

            messages.success(request, f'{theUser.first_name} {theUser.last_name} has been added successfully!')
            form = PasswordResetForm({'email': theUser.email})
            if form.is_valid():
                request = HttpRequest()
                request.META['SERVER_NAME'] = 'www.empoweruomaha.com'
                request.META['SERVER_PORT'] = '80'
                form.save(
                    request=request,
                    from_email=settings.EMAIL_HOST_USER,
                    subject_template_name='registration/new_user_subject.txt',
                    email_template_name='registration/password_reset_newuser_email.html')
            return redirect('/account/users/')

    else:

        sign_form = SignUpForm()

    return render(request, 'account/signupusers.html', {'sign_form': sign_form, 'programs': programs})


@login_required
def reward_category(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = RewardCategoryForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
                cd = form.cleaned_data
                category_name = cd['category']
                messages.success(request, f'{category_name} category added')
                return HttpResponseRedirect('/reward_category')
            elif request.POST.get('category_id'):
                category_id = int(request.POST.get('category_id'))
                category = RewardCategory.objects.get(id=category_id)
                category_name = category.category
                RewardCategory.objects.filter(id=category_id).delete()
                messages.success(request, f'{category_name} category deleted')
                return HttpResponseRedirect('/reward_category')
            else:
                return HttpResponse("Error processing request")
        else:
            form = RewardCategoryForm()
            return render(request, "rewards/reward_categories.html", {'form': form, 'MEDIA_URL': settings.MEDIA_URL})
    else:
        return HttpResponseForbidden(request)

@login_required
def reward_category_edit(request, pk):
    category = get_object_or_404(RewardCategory, id=pk)
    if request.user.is_staff:
        if request.method == 'POST':
            form = RewardCategoryForm(instance=category, data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
                cd = form.cleaned_data
                category_name = cd['category']
                messages.success(request, f'{category_name} category updated')
                return HttpResponseRedirect('/reward_category')
            else:
                return HttpResponse("Error processing request")
        else:
            form = RewardCategoryForm(instance=category)
        return render(request, "rewards/reward_category_edit.html", {'form': form})
    else:
        return HttpResponseForbidden(request)

@login_required
def reward_item(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = RewardItemForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
                cd = form.cleaned_data
                item_name = cd['item']
                messages.success(request, f'{item_name} item added')
                return HttpResponseRedirect('/reward_item')
            elif request.POST.get('item_id'):
                item_id = int(request.POST.get('item_id'))
                item = RewardItem.objects.get(id=item_id)
                item_name = item.item
                RewardItem.objects.filter(id=item_id).delete()
                messages.success(request, f'{item_name} item deleted')
                return HttpResponseRedirect('/reward_item')
            else:
                return HttpResponse("Error processing request")
        else:
            form = RewardItemForm()
            return render(request, "rewards/reward_items.html", {'form': form, 'MEDIA_URL': settings.MEDIA_URL})
    else:
        return HttpResponseForbidden(request)

@login_required
def reward_item_edit(request, pk):
    item = get_object_or_404(RewardItem, id=pk)
    if request.user.is_staff:
        if request.method == 'POST':
            form = RewardItemForm(instance=item, data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
                cd = form.cleaned_data
                item_name = cd['item']
                messages.success(request, f'{item_name} item updated')
                return HttpResponseRedirect('/reward_item')
            else:
                return HttpResponse("Error processing request")
        else:
            form = RewardItemForm(instance=item)
        return render(request, "rewards/reward_items.html", {'form': form})
    else:
        return HttpResponseForbidden(request)

@login_required
def add_school(request):
    addschool = School.objects.all()
    if request.method == 'POST':
        form = SchoolForm(request.POST)
        if form.is_valid():
            school = form.save(commit=False)
            school.save()
            messages.success(request, 'School added successfully')
            return redirect('add_school')
        else:
            messages.error(request, 'Error creating school. Retry!')
            # return HttpResponse('Error updating your profile!')
    else:
        form = SchoolForm()
        # print("Else")
        # profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/add_school.html',
                  {'section': 'add_school', 'form': form, 'addschool': addschool})
