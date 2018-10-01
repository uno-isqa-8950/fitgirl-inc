from django import forms
from django.contrib.auth.models import User
from .models import Profile, Program

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name', 'email')

class UploadFileForm(forms.Form):
    names = []
    count = 0
    d = {}
    for program in Program.objects.all().order_by('program_name'):
        d[program.program_name] = program.program_name
    print(d.items())
    programs = forms.ChoiceField(choices=d.items())
    file = forms.FileField(label=" Choose the CSV file")

class ProfileEditForm(forms.ModelForm):
    date_of_birth = forms.DateField(help_text='Required Format: YYYY-MM-DD')
    class Meta:
        model = Profile
        fields = ('bio', 'date_of_birth', 'age', 'address', 'zip', 'city', 'state', 'day_phone', 'eve_phone', 'age_group', 'school', 'photo')

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ('program_name', 'program_start_date','program_end_date')



