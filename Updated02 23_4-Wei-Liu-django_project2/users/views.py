from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from blog.forms import *
from blog.models import User
from django.db.models import Q


def register(request):
    if request.method == 'POST':
        form = registrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = registrationForm()
    return render(request, 'register.html', {'form': form})


def login(request):
    if request.method =='POST':
        form = loginForm(request.POST)
        if form.is_valid():
            data = request.POST.copy()
            username = data.get('username')
            password = data.get('password')
            if User.objects.filter(Q(username=username)|Q(password=password)):
                return render(request,'register.html')
            else:
                form = loginForm()
    else:
        form = loginForm()
    return render(request,'login.html',{'form':form})



@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile.html', context)

def logout(request):
    return render(request,'logout.html')