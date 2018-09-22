from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserEditForm, ProfileEditForm, ProgramForm, UploadFileForm
from .forms import Profile,User, Program
from .models import ValidUser
from io import TextIOWrapper, StringIO
import csv
from django.contrib import messages

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
                  'account/dashboard.html',
                  {'section': 'dashboard'})

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
            #messages.success(request,' Profile added successfully')
            return HttpResponse('Profile updated successfully!')
        else:
            return HttpResponse('Error updating your profile!')
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


def handle_uploaded_file(request):
          csvf = StringIO(request.FILES['file'].read().decode())
          reader = csv.reader(csvf, delimiter=',')
          reader.__next__();
          count = 0
          for row in reader:
                vu = ValidUser(email = row[1],first_name = row[2],last_name = row[3])
                if vu is not None:
                    vu.save()
                    count = count + 1
          return count



@login_required
def registerusers(request):
    form = request.POST
    program = Program.objects.all().order_by('program_name')
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_name = request.FILES['file']
            validate_csv(file_name)
            value = handle_uploaded_file(request)
            if value > 0:
                form = request.POST
                program = Program.objects.all().order_by('program_name')
                messages.success(request, str(value)+' users added successfully')
    else:
        form = UploadFileForm()
    return render(request,
                  'account/registerusers.html',
                  {'program': program})

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
            return HttpResponse('Profile updated successfully!')
        else:
            return HttpResponse('Error updating your profile!')
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

