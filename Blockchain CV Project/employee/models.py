from django.db import models
from django.contrib.auth.models import User
# from django.contrib.auth.models import User


class Employee(models.Model):
    first_name= models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    unique = models.CharField(max_length=500)
    duration= models.CharField(max_length=500)
    city_of_work = models.CharField(max_length=500)
    work_address = models.CharField(max_length=500)
    company = models.CharField(max_length=500)
    contribution = models.CharField(max_length=500)
    comment_box = models.CharField(max_length=500)


