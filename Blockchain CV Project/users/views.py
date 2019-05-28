from django.shortcuts import render, redirect , HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from blog.forms import *
from blog.models import *
from django.db.models import Q
from blog import views

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
            return redirect('login')
    else:
        form = registrationForm()
    return render(request, 'users/register.html', {'form': form})

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
            if (User.objects.filter(Q(username=username)&Q(password=password))):
                login = User.objects.get(username=username)
                request.session['id'] = login.id
                request.session['type'] = login.roleOfUser
                #Now check the role of user to decide on which page they can view
                if login.roleOfUser.lower() == '1': #redirect to candidate
                    return render(request,'users/employee.html')
                elif login.roleOfUser.lower() == '2':#redirect to employer
                    return render(request,'users/employer.html')
                elif login.roleOfUser.lower() == '3':#redirect to education
                    return render(request,'users/education.html')
            elif employer_education.objects.filter(Q(username=username)&Q(password=password)):
                login = employer_education.objects.get(username=username)
                request.session['id'] = login.id
                request.session['type'] = login.roleOfUser
                #Now check the role of user to decide on which page they can view
                if login.roleOfUser.lower() == 'employer':#redirect to employer
                    return render(request,'users/employer.html')
                elif login.roleOfUser.lower() == 'education':#redirect to education
                    return render(request,'users/education.html')
        
            else:
                form = loginForm()
    else:
        form = loginForm()
    return render(request,'users/login.html',{'form':form})

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
    return render(request,'users/logout.html')


'''
Will allow a user to search for candidates with first name and last name
Check forms.py for the form they search with
'''
def search(request):
    if request.method =='POST':
        form = searchForm(request.POST)
        if form.is_valid():
            data = request.POST.copy()
            fname = data.get('fname').lower()
            sname = data.get('sname').lower()
            if User.objects.filter(Q(fname=fname)&Q(sname=sname)):
                users = User.objects.filter(Q(fname=fname)&Q(sname=sname))
                args = {'users':users}
                return render(request,'users/search.html',args)
            else:
                form = searchForm()
    else:
        form = searchForm()
    return render(request,'users/search.html',{'form':form})

def displayCandidate(request,id):
    if request.method =='POST':
        form = dataForm(request.POST)
        if form.is_valid():
            form.save()
            form = searchForm()
            return redirect('search')
    else:
        user = User.objects.filter(id = id)
        loggedIn = request.session['id']
        form = dataForm(initial={'idOfCandidate': id,'idOfEmployer':loggedIn})
        args = {'user':user,'form':form}
        return render(request,'users/selection.html',args)


# edit_experience funtion
def edit_experience(request):
    if request.method == 'POST':
        id = request.session['id']
        if candidateDetails.objects.filter(user = id):
            print("Hello world")
            candidateDetails.objects.filter(user=id).delete()
            form = experienceForm(request.POST)
            if form.is_valid():
                print("Hello world2")
                form.save()
                return render(request, 'users/added.html')
        else:                    
            form = experienceForm(request.POST) 
            if form.is_valid():
                form.save()
                return render(request, 'users/added.html')
    else:
        loggedIn = request.session['id']
        form = experienceForm(initial ={'user':loggedIn})
    return render(request, 'users/edit_experience.html', {'form':form})



def confirmation(request ,id=None):
    userRole = 'Candidate'
    if checkLoginStatus(request.session['id'],request.session['type'],userRole) == True:
        if id != None:
            deleteEntry(id)
            #return HttpResponseRedirect("")
            return redirect('confirmation')
        else:
            loggedInId = request.session['id']
            userConfirmations = dataEntry.objects.filter(idOfCandidate = loggedInId)
            args = {'item':userConfirmations}
            return render(request,"users/confirmations.html",args)
    else:
        return render(request,'users/nopermission.html')
    
def saveEntry(request,id):
        saved = list(dataEntry.objects.filter(id = id).values_list('entry','fname','sname','instituteName','idOfCandidate','idOfEmployer'))
        args = {'item':saved}
        for item in saved:
            blockAdd(saved,id)
        dataEntry.objects.filter(id = id).delete()
        return render(request,'users/added.html',args)


def deleteEntry(id):
    dataEntry.objects.filter(id = id).delete()


def displayBlock(request):
    args = {'item':blockchain}
    return render(request,'users/testingchain.html',args)

def loadResume(request):
    userRole = 'Candidate'
    if checkLoginStatus(request.session['id'],request.session['type'],userRole) == True:
        currentId = request.session['id']
        resumeOfUser = []
        for item in range(1,len(blockchain)):
            for y in blockchain[item].data:
                if y[4] == currentId:
                    entry = y[0]
                    name = y[1] + y[2]
                    institute = y[3]
                    newlist = [y[0],y[1],y[2],y[3]]
            
                    resume = {
                        'entry':entry,
                        'name':name,
                        'institute':institute,
                        }
                    resumeOfUser.append(newlist)
        args = {'item':resumeOfUser}
        #print(args)
        return render(request,'users/resume.html',args)
    else:
        return render(request,'users/nopermission.html')

            

def checkLoginStatus(id,role,roleToCheckFor):
    if roleToCheckFor == "Candidate":
        if User.objects.filter(Q(id=id)&Q(roleOfUser=role)):
            return True
        else:
            return False
    elif roleToCheckFor == "Employer":
        if User.objects.filter(Q(id=id)&Q(role=roleOfUser)):
            return True
        else:
            return False
    elif roleToCheckFor == "Education":
        if User.objects.filter(Q(id=id)&Q(role=roleOfUser)):
            return True
        else:
            return False
    else:
        return False






'''
blockchain and its related functions below
'''

import hashlib as hasher
import datetime as date
import pickle

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hasher.sha256()
        sha.update((str(self.index) +
        str(self.timestamp) +
        str(self.data) +
        str(self.previous_hash)).encode()) #change here
        return sha.hexdigest()

def create_genesis_block():
 # Manually construct a block with
 # index zero and arbitrary previous hash
 return Block(0, date.datetime.now(), "Genesis Block", "0")



def next_block(last_block,data):
  this_index = last_block.index + 1
  this_timestamp = date.datetime.now()
  this_data = data
  this_hash = last_block.hash
  return Block(this_index, this_timestamp, this_data, this_hash)






# Add blocks to the chain

def blockAdd(content,id):
    for i in range(0, 1):
      previous_block = blockchain[-1]
      block_to_add = next_block(previous_block,content)
      blockchain.append(block_to_add)
      previous_block = block_to_add
      with open("users/save.p","wb") as pickle_out:
          pickle.dump(blockchain,pickle_out)
          pickle_out.close()

# Create the blockchain and add the genesis block or load the previos data
try:
     with open("users/save.p","rb") as pickle_in:
            blockchain = pickle.load(pickle_in)
except EOFError:
    blockchain = [create_genesis_block()]
      
