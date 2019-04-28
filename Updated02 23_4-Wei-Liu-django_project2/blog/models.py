from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

#Created a model to represent a user , role of user is used to specify if they are a candiate , education or employer
#look in forms.py to change the form used to register a user with this model
class User(models.Model):
    username = models.CharField(unique=True,max_length=50)
    fname= models.CharField(max_length=50)
    sname = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    dateOfBirth = models.DateTimeField(default=timezone.now)
    roleOfUser = models.CharField(max_length=9)
    
    def __str__(self):
        return 'Username is {} '.format(self.username)
    
