from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from blog.forms import *
from blog.models import User
from django.db.models import Q

'''
Function lets a user register
Simply checks if the form is valid to the model in the blog folder
then saves it
if its a get request then it sends back the correct form to fill in
check forms.py for the registration form
'''
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

'''
Function for the login system
returns a form if its a Get request
Otherwise it will check that the username and password are correct
Uses the Q module to perform checks on the data
Still needs to redirect to the correct page(employee,employer,education) on correct login
Check forms.py for the login form
'''
def login(request):
    if request.method =='POST':
        form = loginForm(request.POST)
        if form.is_valid():
            data = request.POST.copy()
            username = data.get('username')
            password = data.get('password')
            if User.objects.filter(Q(username=username)&Q(password=password)):
                login = User.objects.get(username=username)
                request.session['id'] = login.id
                request.session['type'] = login.roleOfUser
                #Now check the role of user to decide on which page they can view
                if login.roleOfUser.lower() == 'candidate':
                    return render(request,'employee.html')
                elif login.roleOfUser.lower() == 'employer':
                    return render(request,'employer.html')
                elif login.roleOfUser.lower() == 'education':
                    return render(request,'education.html')
            else:
                form = loginForm()
    else:
        form = loginForm()
    return render(request,'login.html',{'form':form})

'''
This view logs the user out
deletes session data
then redirects them to a page telling them they logged out
'''
def logout(request):
    #mark session as modified so it can be deleted
    request.session.modified = True
    try:
        #delete their session
        del request.session['id']
        del request.session['type']
    except KeyError:
        pass
    #send them to the logout page
    return render(request,'logout.html')


'''
NOT FINISHED
Will allow a user to search for candidates with first name and last name
Check forms.py for the form they search with
'''
def search(request):
    if request.method =='POST':
        form = searchForm(request.POST)
        if form.is_valid():
            data = request.POST.copy()
            fname = data.get('fname')
            sname = data.get('sname')
    else:
        form = searchForm()
        return render(request,'search.html',{'form':form})

def displayCandidate(request):
    users = User.objects.all()
    args = {'users':users}
    return render(request,'search.html',args)


'''
This isnt being used at the moment , was used to display a profile but we arent
using this at the moment
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
'''