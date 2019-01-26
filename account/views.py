from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserEditForm, ProfileEditForm, ProgramForm, UploadFileForm, programArchiveForm
from .forms import Profile,User, Program
from .models import RegisterUser, Affirmations
from io import TextIOWrapper, StringIO
import re

from django.shortcuts import redirect
import csv, string, random
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.forms import ValidationError
from datetime import datetime
import datetime


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

    affirmation = Affirmations.objects.filter(published_date__gte=today).filter(published_date__lt=tomorrow)
    if request.user.is_staff:
        registeredUsers = User.objects.filter(is_superuser=False).order_by('-is_active')
        return render(request, 'account/viewUsers.html', {'registeredUsers': registeredUsers})
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard','affirmation':affirmation})

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
                if re.match(r'^[0-9a-zA-Z_]{1,50}@[0-9a-zA-Z]{1,30}\.[0-9a-zA-Z]{1,3}$', row[1]):
                    if (len(User.objects.all().filter(email=row[1])) > 0):
                        targetUser = User.objects.all().filter(email=row[1])[0]
                        targetUser.is_active = True
                        targetUser.save()
                        targetProfile = targetUser.profile
                        targetProfile.program = Program.objects.all().filter(program_name=name)[0]
                        targetProfile.points = 0
                        targetProfile.pre_assessment = 'No'
                        targetProfile.post_assessment = 'No'
                        targetProfile.save()
                        count += 1

                    else:
                        vu = RegisterUser(email=row[1], first_name=row[2], last_name=row[3], program=name)
                        current_site = get_current_site(request)
                        alphabet = string.ascii_letters + string.digits
                        # theUser = User(username=generate(), password = generate_temp_password(8), first_name = row[2],last_name = row[3], email =row[1])
                        theUser = User(username=vu.email, first_name=row[2], last_name=row[3], email=row[1])
                        theUser.set_password('fitgirl1')
                        theUser.save()
                        profile = Profile.objects.create(user=theUser,
                                                         program=Program.objects.all().filter(program_name=name)[0])
                        profile.save()
                        form = PasswordResetForm({'email': theUser.email})
                        if form.is_valid():
                            request = HttpRequest()
                            request.META['SERVER_NAME'] = 'empoweru.herokuapp.com'
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
            return redirect('edit')
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