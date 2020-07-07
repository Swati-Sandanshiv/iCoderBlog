
from django.shortcuts import render, HttpResponse, redirect # Import redirect so after successfully signup it  should redirect to home
from home.models import Contact
from django.contrib import messages          # To flash messages we import messages
from blog.models import Post
from django.contrib.auth.models import User  # For creating user we need to import user.
from django.contrib.auth import authenticate, login, logout


# HTML Pages-
def home(request):
    return render(request, 'home/home.html')
    # return HttpResponse('This is home')

def about(request):
    return render(request, 'home/about.html')
    # return HttpResponse('This is about')

def contact(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']

        # Validation of Form.
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, 'Please fill the form correctly')
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, 'Your message has been successfully sent')
    return render(request, 'home/contact.html')
    # return HttpResponse('This is contact')

def search(request):
    # From 'base.html' -->'query' is name and id of search form with method 'GET'.
    query = request.GET['query']
    ''' If someone search for a very long query string more than 78 characters, 
        allPosts variable should be blank,else it will show results.'''
    if len(query)>78:
        allPosts = Post.objects.none()
    else:
        '''To view specific post that is been searched in search form, by its title as well as content 
        in that post. This can be done using the 'union' 
        to merge these querysets --> (title__icontains = query) and (content__icontains = query)'''
    allPostsTitle = Post.objects.filter(title__icontains = query)
    allPostsContent = Post.objects.filter(content__icontains = query)
    allPosts = allPostsTitle.union(allPostsContent)
    # To flash message that results are not found.
    if allPosts.count() == 0:
        messages.warning(request,"No search results found. Please refine your query")
    params = {'allPosts': allPosts,'query':query}
    return render(request,'home/search.html',params)
    # return HttpResponse("This is search")

# Authentication APIs-
def handleSignup(request):
    if request.method == 'POST':
        # Get the post parameters from 'SignUp' Modal of 'base.html'.
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Check for errorneous inputs -
        # username should be under 10 characters
        if len(username) > 10:
            messages.error(request,"Username must be under 10 characters")
            return redirect('home')
        
        # username should be alphanumeric
        # 'isalnum()' functions is only for letters and numbers.
        if not username.isalnum(): 
        # username should not contains characters like '@#$*&'.
            messages.error(request,"Username should only contain letters and numbers")
            return redirect('home')
        
        # Password should match
        if pass1 != pass2:
            messages.error(request,"Passwords do not match!")
            return redirect('home')

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your iCoder account has been successfully created")
        return redirect('home')
    else:
        # If someone tries to directly signin without registering form they will get this 404 page.
        return HttpResponse("404 - Not Found") 

def handleLogin(request):
    if request.method == 'POST':
        # Get the post parameters from 'Login' Modal of 'base.html'.
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        # Authenticate 'user' with correct username & password, it will throw error if any one of it is incorrect.
        user = authenticate(username=loginusername, password=loginpassword)

        # If password is wrong the 'user' would be none. 
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials, Please try again")
            return redirect('home')
    # If someone tries to directly login without filling login form they will get this 404 page.
    return HttpResponse("404 - Not Found") 

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('home')


    