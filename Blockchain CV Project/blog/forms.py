from django.forms import *
from .models import *



class registrationForm(ModelForm):
    class Meta:
        model=User
        fields = ['username','fname','sname','password','dateOfBirth','roleOfUser']
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
        fields =['entry','instituteName','fname','sname','idOfCandidate','idOfEmployer']
        widgets = {
            'entry':forms.Textarea,
            'idOfCandidate':forms.HiddenInput,
            'idOfEmployer':forms.HiddenInput,
            }

class experienceForm(ModelForm):
    class Meta:
        model= candidateDetails
        fields = ['user','email','address','gender','phone_number','medicare']
        widgets = {
            'user':forms.HiddenInput,
            }
        def clean(self):
               for field, value in self.cleaned_data.items():
                       self.cleaned_data['user'] = User.objects.filter(id = request.session['id'])
