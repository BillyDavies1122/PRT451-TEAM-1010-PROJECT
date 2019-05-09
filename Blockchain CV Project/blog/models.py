from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django import forms




#Created a model to represent a user , role of user is used to specify if they are a candiate , education or employer
#look in forms.py to change the form used to register a user with this model

RoleChoices = (('1','Candidate'),
               ('2','Employer'),
               ('3','Education'))

class User(models.Model):
    username = models.CharField(unique=True,max_length=50)
    fname= models.CharField(max_length=50)
    sname = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    dateOfBirth = models.DateTimeField(default=timezone.now)
    roleOfUser = models.CharField(max_length=50,choices=RoleChoices)
    medicare = models.DecimalField(max_digits=10,decimal_places=0)
    #String representation of the model
    def __str__(self):
        return 'Username is {}, with Medicare number {} id is {}'.format(self.username,self.medicare,self.id)

    #Makes sure these three fields are saved in lower case by overwriting the save method
    def save(self, *args, **kwargs):
        self.fname = self.fname.lower()
        self.sname = self.sname.lower()
        self.roleOfUser= self.roleOfUser.lower()
        return super(User, self).save(*args, **kwargs)



#Not used yet, potentially used to represent the non candidate roles
class employer_education(models.Model):
    username = models.CharField(unique=True,max_length=50)
    fname= models.CharField(max_length=50)
    sname = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    dateOfBirth = models.DateTimeField(default=timezone.now)
    roleOfUser = models.CharField(max_length=9)
    ABN = models.DecimalField(max_digits=11,decimal_places=0)
    #string representation of the model
    def  __str__(self):
        return 'Username is {} Abn is {} id is {}'.format(self.username,self.ABN,self.id)

    def save(self, *args, **kwargs):
        self.fname = self.fname.lower()
        self.sname = self.sname.lower()
        self.roleOfUser= self.roleOfUser.lower()
        return super(employer_education, self).save(*args, **kwargs)

class dataEntry(models.Model):
    entry = models.TextField()
    idOfCandidate = models.DecimalField(max_digits=10000,decimal_places=0)
    idOfEmployer = models.DecimalField(max_digits=10000,decimal_places=0)

    def __str__(self):
        return '{}'.format(self.entry)




'''
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
'''