
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views

urlpatterns=[
    url('^$',views.welcome,name = 'welcome'),
    url('profile/',views.profile,name='profile'),
    url('update/',views.update_profile,name='update_profile'),
    url(r'^businesses',views.businesses, name='businesses'),
    url(r'^new/business$',views.new_business, name='new_business'),
    url(r'^search/', views.search_businesses, name='search_results'),
    url(r'^post/$', views.post, name='post'),
    url(r'^post/new/$', views.new_post, name='new_post'),

]
