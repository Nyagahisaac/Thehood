from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .email import send_register_confirm_email
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth.decorators import permission_required
from .models import *

# Create your views here.

def registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']

        if password1 == password:
            if User.objects.filter(username=username):
                messages.info(request, 'This Username is taken!')
                return redirect('registration')
            elif User.objects.filter(email=email):
                messages.info(request, 'This Email is taken!')
                return redirect('registration')
            else:
                user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)   
                user.save()           
                
                return redirect('home')
        else:
            messages.info(request,'Passwords should match!')
            return redirect('registration')
    else:
        return render(request,'auth/registration.html')
    
@login_required
def home(request):
    '''
    renders our homepage
    '''
    current_user = get_object_or_404(Profile,user = request.user)
    current_user = Profile.objects.get(user=request.user)
    business = Business.objects.filter(neighbourhood = current_user.neighbourhood)
    user = request.user
    business = Business.objects.filter(neighbourhood=current_user.neighbourhood)
    locations = Neighbourhood.objects.all()
    posts = Post.objects.filter(neighbourhood = current_user.neighbourhood)
    context = {
        'business':business,
        'user':user,
        'current_user':current_user,
        'locations':locations,
        'posts':posts,
        
    }
    return render(request,'all/home.html',context)
        
@login_required
def add_bussiness(request):
    '''
    this view function either renders our add bussiness form our saves a new bussiness
    '''
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        hood = request.POST.get('Location')
        if form.is_valid():
            bussiness = form.save(commit=False)
            bussiness.neighbourhood = hood
            bussiness.posted_by = request.user
            bussiness.save()
            return redirect('home')
        else:
            messages.info(request,"all fields are required")
            return redirect('add-bussiness')
    else:
        current_user = get_object_or_404(Profile,user = request.user)
        current_user = Profile.objects.get(user=request.user)
        business = Business.objects.filter(neighbourhood = current_user.neighbourhood)
        user = request.user
        business = Business.objects.filter(neighbourhood=current_user.neighbourhood)
        locations = Neighbourhood.objects.all()
        form = BusinessForm()
        context = {
            'business':business,
            'user':user,
            'current_user':current_user,
            'locations':locations,
            'form':form,
            
        }
        return render(request,'all/add_bs.html',context)

@login_required
def new_post(request):
    '''
    this is a view function that renders our new post form aswell as save our new post in the db
    '''
    profile = Profile.objects.get(user = request.user)
    hoods = ['Nairobi','Ngong','Ungwaro'
             ,'Thika','Mathare','Juja','Kayole','Dandora']
    if profile.neighbourhood not in hoods:
        messages.info(request,'Provide your neighbourhood information first before adding a post!')
        return redirect('update-profile')
    else:
        if request.method == 'POST':
            form = PostForm(request.POST,request.FILES)
            if form.is_valid():
                post = form.save(commit = False)
                post.posted_by = request.user
                post.neighbourhood = profile.neighbourhood
                post.save()
                return redirect('home')
            else:
                messages.info(request,'All fields are required')
                return redirect('new-post')
        else:
            
            form = PostForm()
            current_user = get_object_or_404(Profile,user = request.user)
            current_user = Profile.objects.get(user=request.user)
            business = Business.objects.filter(neighbourhood = current_user.neighbourhood)
            user = request.user
            business = Business.objects.filter(neighbourhood=current_user.neighbourhood)
            locations = Neighbourhood.objects.all()
            context = {
                'business':business,
                'user':user,
                'current_user':current_user,
                'locations':locations,
                'form':form,
                
            }
            return render(request,'all/new_post.html',context)
            
@login_required
def update_profile(request):
    '''
    this is a view function that handles the update funtionality of our profile
    '''
    
    if request.method == 'POST':
        hood = request.POST.get('Location')
        profileform = UpdateProfileForm(request.POST,request.FILES,instance=request.user.profile)
        userform = UserUpdateform(request.POST,instance=request.user)
        
        if profileform.is_valid() and userform.is_valid():
            profile = profileform.save(commit=False)
            profile.neighbourhood = hood
            profile.user = request.user
            profile.save()
            userform.save()
            return redirect('profile')
        else:
            messages.info(request,'All fields are required!')
            return redirect('update-profile')
    
    else:
        profileform = UpdateProfileForm(instance=request.user.profile)
        userform = UserUpdateform(instance=request.user)
        
        current_user = get_object_or_404(Profile,user = request.user)
        current_user = Profile.objects.get(user=request.user)
        business = Business.objects.filter(neighbourhood = current_user.neighbourhood)
        user = request.user
        business = Business.objects.filter(neighbourhood=current_user.neighbourhood)
        locations = Neighbourhood.objects.all()
        form = BusinessForm()
        context = {
            'business':business,
            'user':user,
            'current_user':current_user,
            'locations':locations,
            'profileform':profileform,
            "userform":userform,
            
        }
        return render(request,'all/update_prof.html',context)
    
@login_required
def profile(request):
    profile = Profile.objects.filter(user= request.user)
    posts = Post.objects.filter(posted_by = request.user)
    
    current_user = get_object_or_404(Profile,user = request.user)
    current_user = Profile.objects.get(user=request.user)
    business = Business.objects.filter(neighbourhood = current_user.neighbourhood)
    user = request.user
    business = Business.objects.filter(neighbourhood=current_user.neighbourhood)
    locations = Neighbourhood.objects.all()
    context = {
        'business':business,
        'user':user,
        'current_user':current_user,
        'locations':locations,
        'profile':profile,
        'posts':posts,
        
    }
    
    return render(request,'all/profile.html',context)
    
#ADMIN DASHBOARD

@login_required()
@permission_required("True","home")
def registered_users(request):
    users = User.objects.all()
    return render(request,'admin_site/users.html',{"users":users})

@login_required()
@permission_required("True","home")
def dashboard(request):
    return render(request,'admin_site/dashboard.html')

@login_required
@permission_required("True","home")
def user_deactivate(request,user_id):
    user = User.objects.get(pk = user_id)
    user.is_active = False
    user.save()
    messages.success(request, f"{user.username}'s account has been deactivated successfully")
    return redirect("system_users")

@login_required()
@permission_required("True","home")
def user_activate(request, user_id):
    user = User.objects.get(pk = user_id)
    user.is_active= True
    user.save()
    messages.success(request,f"{user.username}'s account has been activated succesfull'")
    return redirect('system_users')

#END ADMIN DASHBOARD

@login_required()
def logout_view(request):
    logout(request)
    return redirect('/')

@login_required()
def nav_view(request):
    current_user = Profile.objects.get(user=request.user)
    hoods = ['Nairobi','Ngong','Ruiru'
             ,'Thika','Rwaka','Juja','Kenol','Westlands']
    if profile.neighbourhood not in hoods:
        messages.info(request,'Provide your neighbourhood information first!')
        return redirect('update-profile')
    else:
        current_user = Profile.objects.get(user=request.user)
        business = Business.objects.filter(neighbourhood = current_user.neighbourhood)
        user = request.user
        locations = Neighbourhood.objects.all()
        context = {
            'business':business,
            'user':user,
            'current_user':current_user,
            'locations':locations,
            
        }
        return render(request,'all/navbar.html',context)
    
@login_required()
def location_view(request,id):
    
    current_user = Profile.objects.get(user=request.user)
    business = Business.objects.filter(neighbourhood = current_user.neighbourhood)
    user = request.user
    locations = Neighbourhood.objects.all()  
    location = get_object_or_404(Neighbourhood,id=id)
    occupants = Profile.objects.filter(neighbourhood = location.name)
    business_list = Business.objects.filter(neighbourhood = location.name)
    
    context = {
        'business':business,
        'user':user,
        'current_user':current_user,
        'locations':locations,
        'location':location,
        'occupants':occupants,
        'business_list':business_list
        
    }
    return render(request,'all/single_hood.html',context)


@login_required()
def business_view(request,id):
    bs = get_object_or_404(Business,id=id)
    current_user = Profile.objects.get(user=request.user)
    business = Business.objects.filter(neighbourhood = current_user.neighbourhood)
    
    user = request.user
    locations = Neighbourhood.objects.all()
    context = {
        'business':business,
        'user':user,
        'current_user':current_user,
        'locations':locations,
        'bs':bs,
    }
    return render(request,'all/business.html',context)


  

