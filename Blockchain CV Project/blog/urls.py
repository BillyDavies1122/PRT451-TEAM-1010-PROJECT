#_*_Coding:utf-8_*_
from django.urls import path
from . import views     #. current dictionary
urlpatterns = [
    path('', views.home, name='blog-home'),
    path('employee/', views.employee, name='blog-employee'),
    path('employer/', views.employer, name='blog-employer'),
    path('education/', views.education, name='blog-education'),
    path('employee/confirmation/', views.confirmation, name='blog-confirmation'),
    path('employee/confirmation/work_review/', views.work_review, name='work_review'),
    path('employee/confirmation/education_review/', views.education_review, name='education_review'),
]