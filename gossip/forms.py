from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class UpdateProfile(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['profile_pic','bio','neighbourhood']

class BusinessForm(forms.ModelForm):
    class Meta:
        model=Business
        exclude=['neighbourhood']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['user', 'neighbourhood']      