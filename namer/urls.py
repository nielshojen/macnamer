#from django.conf.urls.defaults import *
from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    #front. page
    url(r'^$', views.index, name='index'),
    #path('index', views.index, name='index'),
    #new group
    url(r'^group/new/', views.new_computer_group, name='new_computer_group'),
    #edit group
    url(r'^group/edit/(?P<group_id>.+)/', views.edit_computer_group),
    #new computer
    url(r'^computer/new/(?P<group_id>.+)/', views.new_computer),
    #edit computer
    url(r'^computer/edit/(?P<computer_id>.+)/', views.edit_computer),
    #delete computer
    url(r'^computer/delete/(?P<computer_id>.+)/', views.delete_computer),
    #new network
    url(r'^network/new/(?P<group_id>.+)/', views.new_network),
    #edit network
    url(r'^network/edit/(?P<network_id>.+)/', views.edit_network),
    #delete network
    url(r'^network/delete/(?P<network_id>.+)/', views.delete_network),
    #show network
    url(r'^network/show/(?P<group_id>.+)/', views.show_network),
    #show group
    url(r'^group/show/(?P<group_id>.+)/', views.show_group),
    #get json info
    url(r'^checkin/', views.checkin),
]
