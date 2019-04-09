from django.shortcuts import render
from .models import Post

# Create your views here.
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request,'blog/home.html',context)


def employee(request):
    return render(request, 'blog/employee.html', {'title': 'employee'})

def employer(request):
    return render(request, 'blog/employer.html', {'title': 'employer'})

def education(request):
    return render(request, 'blog/education.html', {'title': 'education'})
