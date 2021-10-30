from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User


# Create your models here.
class Admin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user

class Neighbourhood(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    no_occupant = HTMLField()
    admin = models.ForeignKey(Admin,on_delete=models.CASCADE)

class User(models.Model):
    name = models.CharField(max_length=100)
    user_id = models.IntegerField(default=1)
    neighbour = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE)
    email = models.EmailField()

class Business(models.Model):
    name = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    neighbour = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE)
    email = models.EmailField()

    def __str__(self):
        return self.name