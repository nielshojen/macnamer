from django.urls import path, include

from rest_framework.routers import DefaultRouter

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from . import views

router = DefaultRouter()
router.register("groups", views.ComputerGroupsViewSet)
router.register("networks", views.NetworksViewSet)
router.register("computers", views.ComputersViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='api:schema'), name='docs'),
]