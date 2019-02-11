from django import forms
from django.contrib.auth.models import User
from .models import Profile, Program
from django.utils.translation import gettext as _
from datetime import date

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your First name'}), max_length=50)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your Last name'}), max_length=50)
    class Meta:
        model = User
        fields = ('first_name','last_name')


def my_choices():
    names = []
    count = 0
    d = {}
    for program in Program.objects.all().order_by('program_name'):
        d[program.program_name] = program.program_name
    return d.items()


class programArchiveForm(forms.Form):



    def __init__(self, *args,**kwargs):
        super(programArchiveForm, self).__init__(*args, **kwargs)
        self.fields['programs'] = forms.ChoiceField(
            choices=my_choices())



class UploadFileForm(forms.Form):


    def __init__(self, *args,**kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.fields['programs'] = forms.ChoiceField(
            choices=my_choices())

    file = forms.FileField(label=" Choose the CSV file")


EVENT = (
    (1, _("8-10")),
    (2, _("11-13")),
)
class ProfileEditForm(forms.ModelForm):
    photo = forms.ImageField(widget=forms.FileInput(attrs={'class':'media'}),required=False)                            #Image field is optional --Shamrose
    bio = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':' Write Something about yourself'}))
    secondary_email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':' Enter secondary email address'}),required=False)
    other_email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':' Enter other email address'}), required=False)
    date_of_birth = forms.DateField(widget=forms.TextInput(attrs={'class':'form-control','type':'date','placeholder':'mm/dd/yyyy format'}))
    zip = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your Zip-Code'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your city name'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your State'}))
    day_phone = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Phone Number'}))
    age_group = forms.ChoiceField(widget=forms.Select, choices=EVENT)
    school = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'School Name'}))


    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        today = date.today()
        if (dob.year + 7, dob.month, dob.day) > (today.year, today.month, today.day):
            raise forms.ValidationError('You must be at least 7 years old to register')
        return dob

    class Meta:
        model = Profile
        fields = ('photo','bio', 'date_of_birth', 'city', 'state', 'zip', 'day_phone', 'age_group', 'school')           # Added Photo to the Start --Shamrose


class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ('program_name', 'program_start_date','program_end_date')

class AdminEditForm(forms.ModelForm):
    photo = forms.ImageField(widget=forms.FileInput(attrs={'class':'media'}),required=False) 
    bio = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':' Write Something about yourself'}))
    date_of_birth = forms.DateField(widget=forms.TextInput(attrs={'class':'form-control','type':'date','placeholder':'mm/dd/yyyy format'}))
    secondary_email = forms.EmailField( widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' Enter secondary email address'}),required=False)
    other_email = forms.EmailField( widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' Enter other email address'}), required=False)
    zip = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your Zip-Code'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your city name'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your State'}))
    day_phone = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Phone Number'}))
    age_group = forms.ChoiceField(widget=forms.Select, choices=EVENT)
    school = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'School Name'}))


    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        today = date.today()
        if (dob.year + 7, dob.month, dob.day) > (today.year, today.month, today.day):
            raise forms.ValidationError('You must be at least 7 years old to register')
        return dob

    class Meta:
        model = Profile
        fields = ('bio', 'date_of_birth', 'city', 'state', 'zip', 'day_phone', 'age_group', 'school')           # Added Photo to the Start --Shamrose


