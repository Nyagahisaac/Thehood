from django.contrib import admin
from .models import Admin,Neighbourhood,User,Business

# Register your models here.
admin.site.register(Admin)
admin.site.register(Neighbourhood)
admin.site.register(User)
admin.site.register(Business)