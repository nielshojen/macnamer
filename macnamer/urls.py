from django.conf.urls import include, url
from django.urls import path
import django.contrib.auth.views as auth_views
from django.contrib.auth.views import LoginView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # url(r'^macnamer/', include('macnamer.foo.urls')),
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    #path('login/', LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.logout_then_login, name='login'),
    #path('logout/', auth_views.logout_then_login, name='logout'),
    url(r'^changepassword/$', auth_views.PasswordChangeView.as_view(), name='changepassword'),
    url(r'^changepassword/done/$', auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
   	#url(r'^', include('namer.urls')),
   	path('', include('namer.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', admin.site.urls),
    #url(r'^$', 'namer.views.index', name='home'),
]
