from .models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django import forms

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1')

class UserUpdateForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=200)
    last_name = forms.CharField(label='Last Name', max_length=200)
    bio = forms.CharField(label='Bio', max_length=500)
    profile_picture = forms.URLField(label='Profile Picture Url')