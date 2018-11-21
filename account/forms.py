from django import forms
from django.contrib.auth.models import User
from .models import Profile, Program
from django.utils.translation import gettext as _

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your First name'}), max_length=50)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your Last name'}), max_length=50)
    #email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':' Enter your email address'}))
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
    photo = forms.ImageField(widget=forms.FileInput(attrs={'class':'media'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':' Write Something about yourself'}))
    date_of_birth = forms.DateField(widget=forms.TextInput(attrs={'class':'form-control','type':'date','placeholder':'mm/dd/yyyy format'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Enter your Address'}))
    zip = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your Zip-Code'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your city name'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your State'}))
    day_phone = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Phone Number'}))
    eve_phone = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Phone Number'}))
    age_group = forms.ChoiceField(widget=forms.Select, choices=EVENT)
    school = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'School Name'}))
    class Meta:
        model = Profile
        fields = ('photo', 'bio', 'date_of_birth', 'address', 'zip', 'city', 'state', 'day_phone', 'eve_phone', 'age_group', 'school')

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ('program_name', 'program_start_date','program_end_date')



