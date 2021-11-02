from django.db import models
from django.db.models.fields import IntegerField, TextField
from tinymce.models import HTMLField
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    '''
    this is a class that defines the profile structure of our user
    '''
    user = models.OneToOneField(User,on_delete = models.CASCADE)    
    profile_pic = models.ImageField(upload_to= 'images/', default= 'default.jpg')
    bio = HTMLField()
    neighbourhood = models.CharField(max_length=200)

    
    def __str__(self):
        return self.user.username

        return self.user.username


class Business(models.Model):
    '''
    this class gives a blueprint how our bussinesses will be made
    '''
    posted_by = models.ForeignKey(User,on_delete = models.CASCADE)
    neighbourhood = models.CharField(max_length=100)
    email = models.EmailField()
    name = models.CharField(max_length=250)
    description = TextField()
    image =  models.ImageField(upload_to= 'post/', default= 'default.jpg')
    
    def __str__(self):
        return self.name

class Post(models.Model):
    '''
    this creates the blueprint on which the post will rely on
    '''
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to= 'post/',blank=True)
    description = TextField()
    posted_by = models.ForeignKey(User,on_delete= models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add=True)
    neighbourhood = models.CharField(max_length= 100)
    
    def __str__(self):
        return self.title

class Neighbourhood(models.Model):
    '''
    this is used to create the neighbourhood information
    '''
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to= 'post/',blank=True)
    
    def __str__(self):
        return self.name