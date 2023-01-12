from django.urls import path, include
import django.contrib.auth.views as auth_views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.logout_then_login, name='logout'),
    path('changepassword/', auth_views.PasswordChangeView.as_view(), name='changepassword'),
    path('changepassword/done/', auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
   	path('', include('namer.urls')),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
]
