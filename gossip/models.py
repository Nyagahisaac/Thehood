from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import Admin


# Create your models here.
class Neighbourhood(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    no_occupant = HTMLField()
    admin = models.ForeignKey(Admin,on_delete=models.CASCADE)