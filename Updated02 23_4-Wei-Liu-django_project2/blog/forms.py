from django.forms import *
from django import forms
from .models import *


class registrationForm(ModelForm):
    class Meta:
        model=User
        fields = ['username','fname','sname','password','dateOfBirth','roleOfUser']


class loginForm(forms.Form):
        username = forms.CharField(label = 'username')
        password = forms.CharField(label = 'password')

class searchForm(forms.Form):
    fname = forms.CharField(label = 'fname')
    sname = forms.CharField(label = 'sname')
