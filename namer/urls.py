from django.urls import path

from . import views

urlpatterns = [
    #front. page
    path('', views.index, name='index'),
    #new group
    path('group/new/', views.new_computer_group, name='new_computer_group'),
    #edit group
    path('group/edit/<int:group_id>/', views.edit_computer_group, name='edit_computer_group'),
    #new computer
    path('computer/new/<int:group_id>/', views.new_computer, name='new_computer'),
    #edit computer
    path('computer/edit/<int:computer_id>/', views.edit_computer, name='edit_computer'),
    #delete computer
    path('computer/delete/<int:computer_id>/', views.delete_computer, name='delete_computer'),
    #new network
    path('network/new/(<int:group_id>/', views.new_network, name='new_network'),
    #edit network
    path('network/edit/<int:network_id>/', views.edit_network, name='edit_network'),
    #delete network
    path('network/delete/<int:network_id>/', views.delete_network, name='delete_network'),
    #show network
    path('network/show/<int:group_id>/', views.show_network, name='show_network'),
    #show group
    path('group/show/<int:group_id>/', views.show_group, name='show_group'),
    #get json info
    path('checkin/', views.checkin, name='checkin'),
]
