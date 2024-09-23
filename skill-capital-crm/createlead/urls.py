from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreateLeadsViewSet

router = DefaultRouter()

router.register(r'leads1', CreateLeadsViewSet)

urlpatterns = [
    path('', include(router.urls))
]