from django.shortcuts import render
#from .models import Post
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

def confirmation(request):
    # return HttpResponse('<h1> confirmation </h1>')
    return render(request, 'blog/confirmation.html', {'title': 'confirmation'})
def work_review(request):
    # return HttpResponse('<h1> confirmation </h1>')
    return render(request, 'blog/work_review.html', {'title': 'work_review'})
def education_review(request):
    # return HttpResponse('<h1> confirmation </h1>')
    return render(request, 'blog/education_review.html', {'title': 'education_review'})