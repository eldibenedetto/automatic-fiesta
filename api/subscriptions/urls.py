from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomerViewSet

router = DefaultRouter()
router.register("subscriptions", CustomerViewSet,basename="customer")
urlpatterns = [path("v1/", include(router.urls))]