from django import forms
from django.contrib.auth.models import User
from .models import Profile, Program, Parameters, RewardCategory, RewardItem
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
    print(d)
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
    secondary_email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your secondary email (optional)'}),required=False)
    other_email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your other email (optional)'}),required=False)
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
        fields = ('photo','bio', 'secondary_email','other_email', 'date_of_birth', 'city', 'state', 'zip', 'day_phone', 'age_group', 'school')           # Added Photo to the Start --Shamrose


class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ('program_name', 'program_start_date','program_end_date')

class CronForm(forms.Form):
    days = forms.ChoiceField(choices=[(x,x) for x in range(1,32)])


class RewardsNotificationForm(forms.Form):
    Rewards_milestone_1 = forms.IntegerField(required=True)
    Rewards_milestone_2 = forms.IntegerField(required=True)
    Rewards_milestone_3 = forms.IntegerField(required=True)
    Rewards_milestone_4 = forms.IntegerField(required=True)

class ManagePointForm(forms.Form):

    #programs = forms.ModelChoiceField(queryset=Program.objects.all().order_by('program_name'))
    #users = forms.ModelChoiceField(queryset=User.objects.filter(is_superuser=False).order_by('username'))
    manage_points = forms.IntegerField(required=True)

class AdminEditForm(forms.ModelForm):
    photo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'media'}), required=False)  # Image field is optional --Shamrose
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': ' Write Something about yourself'}))
    date_of_birth = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'mm/dd/yyyy format'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Address'}))
    zip = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Zip-Code'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your city name'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your State'}))
    day_phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))


    class Meta:
        model = Profile
        fields = ('photo', 'bio', 'date_of_birth', 'address', 'city', 'state', 'zip', 'day_phone')


class EmailForm(forms.Form):
    subject = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter Subject'}))
    message = forms.CharField(required=False,
                              widget=forms.Textarea(attrs={'placeholder': 'Select "Text" below to send this message or'
                                                                          'Select "CMS template" to send content from CMS'}))

class ContactForm(forms.Form):
    subject = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    message = forms.CharField(required=True, widget=forms.Textarea)

class ParametersForm(forms.ModelForm):
    class Meta:
        model = Parameters
        fields = ('physical_days_to_done', 'nutrition_days_to_done')


class ProgramClone(forms.Form):
    def program_list():
        my_program_list = list()

        for item in Program.objects.all():
            tuple = (item.id, item.program_name)
            my_program_list.append(tuple)

        return my_program_list

    program_to_clone = forms.ChoiceField(choices=program_list,
                                         label="Choose a Program to Clone",
                                         )
    new_start_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                   'type': 'date',
                                                                   'placeholder': 'mm/dd/yyyy format'}))
    new_program = forms.CharField(max_length=50,
                                  label="Name of New Program")

    fields = (program_to_clone, new_start_date, new_program)


class SignUpForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('email','first_name', 'last_name')

class RewardCategory(forms.ModelForm):
    class Meta:
        model = RewardCategory
        fields = ('category', 'description', 'image')

class RewardItem(forms.ModelForm):
    class Meta:
        model = RewardItem
        fields = ('item', 'description', 'points_needed', 'qty_available', 'image', 'category')
