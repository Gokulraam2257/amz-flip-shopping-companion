from django import forms
from django.contrib.auth.forms import *
from django.contrib.auth.models import User
from .models import *
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password1', 'password2']


class UserloginForm(UserCreationForm):
    
    
    class Meta:
        model = User
        fields = ['username', 'password1']

class UserDetailsForm(forms.ModelForm):  
    
    class Meta:
        model = UserProfile
        fields = ['purchase_limit','whatsapp_number']