from django.urls import path

# from . import key_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("keys/", views.api_key_list, name="api_keys_list"),
    path("keys/new/", views.api_key_create, name="api_keys_create"),
    path("keys/<str:pk>/revoke/", views.api_key_revoke, name="api_keys_revoke"),
    path("keys/<str:prefix>/delete/", views.api_key_delete, name="api_keys_delete"),
    path('group/new/', views.new_computer_group, name='new_computer_group'),
    path('group/edit/<int:group_id>/', views.edit_computer_group, name='edit_computer_group'),
    path('computer/new/<int:group_id>/', views.new_computer, name='new_computer'),
    path('computer/edit/<int:computer_id>/', views.edit_computer, name='edit_computer'),
    path('computer/delete/<int:computer_id>/', views.delete_computer, name='delete_computer'),
    path('network/new/(<int:group_id>/', views.new_network, name='new_network'),
    path('network/edit/<int:network_id>/', views.edit_network, name='edit_network'),
    path('network/delete/<int:network_id>/', views.delete_network, name='delete_network'),
    path('network/show/<int:group_id>/', views.show_network, name='show_network'),
    path('group/show/<int:group_id>/', views.show_group, name='show_group'),
    path('checkin/', views.checkin, name='checkin'),
]
