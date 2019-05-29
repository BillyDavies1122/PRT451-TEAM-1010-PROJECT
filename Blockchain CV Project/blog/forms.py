from django.forms import *
from .models import *



class registrationForm(ModelForm):
    class Meta:
        model=User
        fields = ['username','fname','sname','password','dateOfBirth','roleOfUser']
        widgets = {
            'password':forms.PasswordInput(),
            }
        labels = {
            "fname": "First Name",
            "sname": "Surname",
            "dateOfBirth": "Date of Birth",
            "roleOfUser":"Select your Role"
            }



class loginForm(forms.Form):
        username = forms.CharField(label = 'Username')
        password = forms.CharField(label = 'Password',widget=forms.PasswordInput())


class searchForm(forms.Form):
    fname = forms.CharField(label = 'First Name')
    sname = forms.CharField(label = 'Surname')


class dataForm(ModelForm):
    class Meta:
        model=dataEntry
        fields =['entry','instituteName','fname','sname','idOfCandidate','idOfEmployer']
        widgets = {
            'entry':forms.Textarea,
            'idOfCandidate':forms.HiddenInput,
            'idOfEmployer':forms.HiddenInput,
            }

        labels = {
            "entry":"Enter work details for the candidate , include all relevant information",
            "fname": "Your First Name",
            "sname": "Your Surname",
            "instituteName":"Name of company you work for"

            }

class experienceForm(ModelForm):
    class Meta:
        model= candidateDetails
        fields = ['user','email','address','gender','phone_number','medicare']
        widgets = {
            'user':forms.HiddenInput,
            }
        labels = {
            "email":"Email Address",
            "address":"Home Address",
            "gender":"Gender",
            "phone_number":"Phone Number",
            "medicare":"Medicare Number",
            }

        def clean(self):
               for field, value in self.cleaned_data.items():
                       self.cleaned_data['user'] = User.objects.filter(id = request.session['id'])
