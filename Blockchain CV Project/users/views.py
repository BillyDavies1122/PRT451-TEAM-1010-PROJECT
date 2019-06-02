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
Written by Billy Davies
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
Written by Billy Davies
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
                try:
                    #delete their session
                    del request.session['id']
                    del request.session['type']
                except KeyError:
                    pass
                form = loginForm()
    else:
        form = loginForm()
    return render(request,'users/login.html',{'form':form})

'''
This view logs the user out
deletes session data
then redirects them to a page telling them they logged out
Written by Billy Davies
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

If the request isnt a post it sends a simple form to the template
if its a post request it gets the fname and sname elements and makes it lower case, 
then it  searches the database for anyone called that and sends a dict with all users it found to the template to be rendered
Written by Billy Davies
'''
def search(request):
    #checks permission
    if checkLoginStatus(request.session['id'],request.session['type'],'employer') or checkLoginStatus(request.session['id'],request.session['type'],'education') == True:
        if request.method =='POST':
            form = searchForm(request.POST)
            if form.is_valid():
                #gets data from post 
                data = request.POST.copy()
                #set names to lowercase
                fname = data.get('fname').lower()
                sname = data.get('sname').lower()
                #if  that user exists
                if User.objects.filter(Q(fname=fname)&Q(sname=sname)):
                    #create a query object and add to dict then send back to be rendered
                    users = User.objects.filter(Q(fname=fname)&Q(sname=sname))
                    args = {'users':users}
                    return render(request,'users/search.html',args)
                else:
                    form = searchForm()
        else:
            form = searchForm()
        return render(request,'users/search.html',{'form':form})
    else:
        #send them here if  they done have permission
        return render(request,'users/nopermission.html')


'''
This function is used to write and save entries about a selected candidate
It takes in a candidates id and a request
If the user has permission and the request is not a POST it will first send  create a form to send to the template specified with the id of the candidate and the person entering already filled in
When a user submits the form it then checks its valid and saves it. then it  redirects you  have to the search page
Written by Billy Davies
'''
def displayCandidate(request,id):
    #check permissions
    if checkLoginStatus(request.session['id'],request.session['type'],'employer') or checkLoginStatus(request.session['id'],request.session['type'],'education') == True:
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
    else:
        #if no permission redirect them here
        return render(request,'users/nopermission.html')

# edit_experience funtion
'''
This function allows a candidate to edit their information
If the user has already added data about them , it edits that data. 
otherwise it creates an entry linked to their account with their extra details
Written by Billy Davies
'''
def edit_experience(request):
    if checkLoginStatus(request.session['id'],request.session['type'],'candidate') == True:
        if request.method == 'POST':
            id = request.session['id']
            #if they have already got an entry saved delete the current one and save the new one
            if candidateDetails.objects.filter(user = id):
               
                candidateDetails.objects.filter(user=id).delete()
                form = experienceForm(request.POST)
                if form.is_valid():
                    form.save()
                    return render(request, 'users/added.html')
            #if not then we add one
            else:                    
                form = experienceForm(request.POST) 
                if form.is_valid():
                    form.save()
                    return render(request, 'users/added.html')
        else:
            loggedIn = request.session['id']
            form = experienceForm(initial ={'user':loggedIn})
        return render(request, 'users/edit_experience.html', {'form':form})
    else:
        return render(request,'users/nopermission.html')

'''
This function checks if a user has any pending confirmations
then can accept or deny them
Written by Billy Davies
'''

def confirmation(request ,id=None):
    userRole = 'candidate'
    #if they have permission
    if checkLoginStatus(request.session['id'],request.session['type'],'candidate') == True:
        #if the id is not none then they must be deleteing
        if id != None:
            #delete the entry
            deleteEntry(id)
            return redirect('confirmation')
        else:
            #get all confirmations this user may have
            loggedInId = request.session['id']
            userConfirmations = dataEntry.objects.filter(idOfCandidate = loggedInId)
            args = {'item':userConfirmations}
            return render(request,"users/confirmations.html",args)
    else:
        #if not redirect them here
        return render(request,'users/nopermission.html')

'''
This function saves an entry
it takes in the id of an entry
then saves it to the blockchain using the blockAdd function
Written by Billy Davies
'''
def saveEntry(request,id):
        #Creates a list object out of the needed entry
        saved = list(dataEntry.objects.filter(id = id).values_list('entry','fname','sname','instituteName','idOfCandidate','idOfEmployer'))
        #adds the list to a dict
        args = {'item':saved}
        #saves all the i tems in the dict
        for item in saved:
            blockAdd(saved,id)
        #deltes  the entry as its not saved and we dont need it anymore
        dataEntry.objects.filter(id = id).delete()
        #display the added page
        return render(request,'users/added.html',args)

'''
Takes in an id and deletes the associated entry
Written by Billy Davies
'''
def deleteEntry(id):
    dataEntry.objects.filter(id = id).delete()

'''
displays all blocks in the chain
not meant for use outside of demonstrations and trouble shooting
Written by Billy Davies
'''
def displayBlock(request):
    args = {'item':blockchain}
    return render(request,'users/testingchain.html',args)

'''
Function used to load logged in users resumes
loops through the blockchain finding all relevant blocks
then sends it to a template to be rendered
Written by Billy Davies
'''
def loadResume(request):
    userRole = 'candidate'
    #if they have permssion
    if checkLoginStatus(request.session['id'],request.session['type'],userRole) == True:
        currentId = request.session['id']
        resumeOfUser = []
        #loop through the blockchain
        for item in range(1,len(blockchain)):
            for y in blockchain[item].data:
                #if the id of candidate is in the block add all the data to a list
                if y[4] == currentId:
                    entry = y[0]
                    name = y[1] + y[2]
                    institute = y[3]
                    newlist = [y[0],y[1],y[2],y[3]]
                   #add to another list
                    resumeOfUser.append(newlist)
        #add the list to a dictionary
        args = {'item':resumeOfUser}
        #return the dict to be rendered
        return render(request,'users/resume.html',args)
    else:
        #user didnt have permission
        return render(request,'users/nopermission.html')

'''
Used to search through candidates as education and employer type user
works the same as the other search function but its redirecting to a different page
Written by Billy Davies
'''
def searchResumes(request):
    if checkLoginStatus(request.session['id'],request.session['type'],'employer') or checkLoginStatus(request.session['id'],request.session['type'],'education') == True:
        if request.method =='POST':
            form = searchForm(request.POST)
            if form.is_valid():
                data = request.POST.copy()
                fname = data.get('fname').lower()
                sname = data.get('sname').lower()
                if User.objects.filter(Q(fname=fname)&Q(sname=sname)):
                    users = User.objects.filter(Q(fname=fname)&Q(sname=sname))
                    args = {'users':users}
                    return render(request,'users/searchResume.html',args)
                else:
                    form = searchForm()
        else:
            form = searchForm()
        return render(request,'users/search.html',{'form':form})
    else:
        return render(request,'users/nopermission.html')


'''
used by employers and education to load a candidates resume
Loops through the blockchain checking for the specified Id
Sends a dict containing a list of lists to the template to be rendered
Written by Billy Davies

'''
def loadCandidateResume(request,id):
    candidateId = id
    resumeOfUser = []
    for item in range(1,len(blockchain)):
            for y in blockchain[item].data:
                if y[4] == candidateId:
                    entry = y[0]
                    name = y[1] + y[2]
                    institute = y[3]
                    newlist = [y[0],y[1],y[2],y[3]]
                    resumeOfUser.append(newlist)
    args = {'item':resumeOfUser}
    return render(request,'users/resumeEduEmp.html',args)

            
'''
This function checks whether a user is allowed access to pages when it  is called
It takes in the users id , their role and the role we are checking for
written by Billy Davies
'''
def checkLoginStatus(id,role,roleToCheckFor):
    #if candidate
    if roleToCheckFor == 'candidate':
        if User.objects.filter(Q(id=id)&Q(roleOfUser='1')):
            
            return True
        else:
            return False
    # if employer
    elif roleToCheckFor == 'employer':
        if User.objects.filter(Q(id=id)&Q(roleOfUser='2')):
            
            return True
        else:
            return False
    # if education
    elif roleToCheckFor == 'education':
        
        if User.objects.filter(Q(id=id)&Q(roleOfUser='3')):
           
            return True
        else:
            return False
    else:
        return False






'''
blockchain and its related functions below
used https://medium.com/crypto-currently/lets-build-the-tiniest-blockchain-e70965a248b to help create it
'''

import hashlib as hasher
import datetime as date
import pickle

class Block:
    '''
     initialise the block
     block has a index
     block has the timestamp it was made
     block has the data it contains
     block has the hash of the previous block
     block has its own hash

    '''
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        #generate a sha256 hash
        sha = hasher.sha256()
        #update hash object with items
        sha.update((str(self.index) +
            str(self.timestamp) +
            str(self.data) +
            str(self.previous_hash)).encode())
        #return the hash as a string type
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
'''
This function adds blocks passed through to it to the chain, then saves the blockchain using the pickle library to a file
Written by Billy Davies
'''
def blockAdd(content,id):
    for i in range(0, 1):
      previous_block = blockchain[-1]
      block_to_add = next_block(previous_block,content)
      blockchain.append(block_to_add)
      previous_block = block_to_add
      with open("users/save.p","wb") as pickle_out:
          pickle.dump(blockchain,pickle_out)
          pickle_out.close()

# Create the blockchain and add the genesis block or load the previos data from the pickle file if its not empty
try:
     with open("users/save.p","rb") as pickle_in:
            blockchain = pickle.load(pickle_in)
except EOFError:
    blockchain = [create_genesis_block()]
      
