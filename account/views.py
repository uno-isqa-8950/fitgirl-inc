from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserEditForm, ProfileEditForm, ProgramForm, UploadFileForm
from .forms import Profile,User, Program
from .models import ValidUser
from io import TextIOWrapper, StringIO



import csv, string, random
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings


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
    return render(request,
                  'account/userdashboard.html',
                  {'section': 'dashboard'})

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
            print ("program_form")
            program= form.save(commit=False)
            #program.created_date = timezone.now()
            program.save()
            messages.success(request,' Program added successfully')
            #return HttpResponse('Program added successfully!')
        else:
            messages.error(request, ('Error updating program'))
            #return HttpResponse('Error updating your profile!')
    else:
        form = ProgramForm()
        print("Else")
        #profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/createprogram.html',
                  {'section': 'createprogram','form':form,'registeredPrograms':registeredPrograms})


def validate_csv(value):
    if not value.name.endswith('.csv'):
        raise ValidationError('Invalid file type')


def handle_uploaded_file(request, name):
          csvf = StringIO(request.FILES['file'].read().decode())
          reader = csv.reader(csvf, delimiter=',')
          reader.__next__();
          count = 0
          for row in reader:
                vu = ValidUser(email = row[1],first_name = row[2],last_name = row[3],program=name)
                current_site = get_current_site(request)
                alphabet = string.ascii_letters + string.digits
                # theUser = User(username=generate(), password = generate_temp_password(8), first_name = row[2],last_name = row[3], email =row[1])
                theUser = User(username=vu.email, first_name=row[2], last_name=row[3], email=row[1])
                theUser.set_password('fitgirl1')
                theUser.save()
                form = PasswordResetForm({'email': theUser.email})
                if form.is_valid():
                    request = HttpRequest()
                    request.META['SERVER_NAME'] = current_site
                    request.META['SERVER_PORT'] = '80'
                    form.save(
                        request=request,
                        from_email=settings.EMAIL_HOST_USER,
                        subject_template_name='registration/new_user_subject.txt',
                        email_template_name='registration/password_reset_newuser_email.html')
                if vu is not None:
                    vu.save()
                    count = count + 1
          return count


def get_short_name(self):
    # The user is identified by their email address
    return self.first_name


@login_required
def registerusers(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_name = request.FILES['file']
            validate_csv(file_name)
            value = handle_uploaded_file(request,form.cleaned_data['programs'])

            if value > 0:
                form = request.POST
                messages.success(request, str(value)+' users added successfully')
    else:
        form = UploadFileForm()
    return render(request,
                  'account/registerusers.html',
                  {'form' : form})

@login_required
def aboutus(request):
    return render(request,
                  'account/aboutus.html',
                  {'section': 'aboutus'})

@login_required
def users(request):
    registeredUsers = ValidUser.objects.all()
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
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            #return HttpResponseRedirect('Profile updated successfully!')
            messages.success(request, ('Your profile was updated successfully.'))
            #print("hi")
            #return render(request,'account/dashboard.html')
        else:
            messages.error(request,('Please correct the error below.'))
            #return HttpResponse('Error updating your profile!')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


@login_required
def profile(request):
    return render(request,
                  'account/profile.html',
                  {'section': 'profile'})

