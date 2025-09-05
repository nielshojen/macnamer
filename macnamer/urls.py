from django.urls import path, include, re_path
import django.contrib.auth.views as auth_views

from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.logout_then_login, name='logout_then_login'),
    path('changepassword/', auth_views.PasswordChangeView.as_view(), name='changepassword'),
    path('changepassword/done/', auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
   	path('', include('namer.urls')),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/', include(('api.v1.urls', 'api'), namespace='api')),
    # path("api/v1/", include(("api.v1.urls", "apiv1"), namespace="apiv1")),
    path('health/', include('health_check.urls'), name='health'),
    re_path(r'^saml2/', include('djangosaml2.urls')),
]
