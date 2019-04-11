#_*_Coding:utf-8_*_
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('employee/', views.employee, name='blog-employee'),
    path('employer/', views.employer, name='blog-employer'),
    path('education/', views.education, name='blog-education'),
]