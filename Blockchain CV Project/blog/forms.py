from django.forms import *
from .models import *



class registrationForm(ModelForm):
    class Meta:
        model=User
        fields = ['username','fname','sname','password','dateOfBirth','roleOfUser','medicare']
        widgets = {
            'password':forms.PasswordInput(),
            }



class loginForm(forms.Form):
        username = forms.CharField(label = 'username')
        password = forms.CharField(label = 'password',widget=forms.PasswordInput())

class searchForm(forms.Form):
    fname = forms.CharField(label = 'fname')
    sname = forms.CharField(label = 'sname')


class dataForm(ModelForm):
    class Meta:
        model=dataEntry
        fields =['entry','idOfCandidate','idOfEmployer']
        widgets = {
            'entry':forms.Textarea,
            'idOfCandidate':forms.HiddenInput,
            'idOfEmployer':forms.HiddenInput,
            }

class experienceForm(ModelForm):
    class Meta:
        model=employer_experience
        fields = ['email','address','gender','phone_number','comment_box']


