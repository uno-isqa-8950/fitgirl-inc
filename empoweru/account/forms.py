from django import forms
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class ProfileEditForm(forms.ModelForm):
    date_of_birth = forms.DateField(help_text='Required.Format: YYYY-MM-DD')
    class Meta:
        model = Profile
        fields = ('first_name','last_name','email','date_of_birth', 'photo')