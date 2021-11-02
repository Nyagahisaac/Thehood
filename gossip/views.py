
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages
from .models import *
from django.http import HttpResponseRedirect

# Create your views here.
@login_required(login_url='/accounts/login/')
def welcome(request):
    current_user = request.user
    hoods = Neighbourhood.get_all_hoods()
    return render (request, 'home.html', {"hoods":hoods})

@login_required
def profile(request):
  current_user = request.user
  return render(request,'profile.html') 


@login_required(login_url='/accounts/login/')
def update_profile(request):
    current_user=request.user
    if request.method=="POST":
        instance = Profile.objects.get(user=current_user)
        form =UpdateProfile(request.POST,request.FILES,instance=instance)
        if form.is_valid():
            profile = form.save(commit = False)
            profile.user = current_user
            profile.save()

        return redirect('/profile')

    elif Profile.objects.get(user=current_user):
        profile = Profile.objects.get(user=current_user)
        form = UpdateProfile(instance=profile)
    else:
        form = UpdateProfile()

    return render(request,'update_profile.html',{"form":form}) 
 
@login_required(login_url='/accounts/login/')
def businesses(request):
    current_user=request.user
    businesses = Business.objects.all()
    

    return render(request,'businesses.html',{"businesses":businesses}) 


@login_required(login_url='/accounts/login/')
def new_business(request):
    current_user=request.user
    profile =Profile.objects.get(user=current_user)

    if request.method=="POST":
        form =BusinessForm(request.POST,request.FILES)
        if form.is_valid():
            business = form.save(commit = False)
            business.owner = current_user
            print('*******************************************************************************************')
            print(profile.neighbourhood)
            business.neighbourhood = profile.neighbourhood
            business.save()

        return HttpResponseRedirect('/businesses')

    else:
        form = BusinessForm()

    return render(request,'newbusiness.html',{"form":form})

@login_required(login_url='/accounts/login/')
def search_businesses(request):
    if 'keyword' in request.GET and request.GET["keyword"]:
        search_term = request.GET.get("keyword")
        searched_projects = Business.search_business(search_term)
        message = f"{search_term}"

        return render(request, 'search.html', {"message":message,"businesses": searched_projects})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html', {"message": message})   

@login_required(login_url='/accounts/login')
def post(request):
    current_user = request.user
    post = Post.get_all_posts()
    return render(request, 'post.html', {"post": post})      

@login_required(login_url='/accounts/login')
def new_post(request):
    
    profile = Profile.objects.get(user = request.user)
    
    if request.method == 'POST':
        
        form = PostForm(request.POST)
        
        if form.is_valid():
            
            post = form.save(commit = False)
            post.user = request.user
            post.neighbourhood = profile.neighbourhood
            post.save()
            
        return redirect('/')
    
    else:
        
        form = PostForm()
        
    return render(request, 'new_post.html', {"profile": profile, "form": form})    