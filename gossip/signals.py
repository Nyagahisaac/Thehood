from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save,sender = User)
def create_profile(sender,instance,created,**kwargs):
    '''
    this is a function that creates a profile for user on registration
    '''
    if created:
        Profile.objects.create(user = instance)
    
@receiver(post_save, sender=User)
def save_profile(sender,instance,**kwargs):
    '''
    this is a function that saves the profile once created after registration
    '''
    instance.profile.save()