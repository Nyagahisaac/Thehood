
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views

urlpatterns=[
    url('^$',views.welcome,name = 'welcome'),
    url('profile/',views.profile,name='profile'),
    url('update/',views.update_profile,name='update_profile'),
    ,

]
