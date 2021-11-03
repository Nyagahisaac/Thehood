from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class Neighbourhood(models.Model):
    neighbourhood = models.CharField(max_length=100)
    image = models.ImageField(upload_to='photo/',blank=True)
    occupants = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.neighbourhood

    def save_neighbourhood(self):
        self.save()

    @classmethod
    def get_all_hoods(cls):
        hoods = Neighbourhood.objects.all()
        return hoods

    @classmethod
    def delete_neighbourhood(cls,neighbourhood):
        cls.objects.filter(neighbourhood=neighbourhood).delete()

class Profile(models.Model):
  profile_pic = models.ImageField(default='../static/images/default.jpeg',upload_to='media/')
  neighbourhood = models.ForeignKey(Neighbourhood,on_delete=models.CASCADE,null=True)
  bio = models.TextField()
  user = models.OneToOneField(User,on_delete = models.CASCADE)
  neighbourhood = models.CharField(max_length=30, null=True)
  
  @receiver(post_save , sender = User)
  def create_profile(instance,sender,created,**kwargs):
    if created:
      Profile.objects.create(user = instance)

  @receiver(post_save,sender = User)
  def save_profile(sender,instance,**kwargs):
    instance.profile.save()

  def __str__(self):
    return self.user


class Business(models.Model):
    name =models.CharField(max_length=100)
    description = models.TextField()
    neighbourhood = models.ForeignKey(Neighbourhood,on_delete=models.CASCADE,null=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    email = models.EmailField()
    address =models.CharField(max_length=100)
    contact = models.IntegerField()

    def __str__(self):
        return self.name

    @classmethod
    def search_business(cls, search_term):
        business = cls.objects.filter(name__icontains=search_term)
        return business
        
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True, null=True)
    
    
    def __str__(self):
        
        return self.title

    @classmethod
    def get_all_posts(cls):
        post = Post.objects.all()
        return post 

  

