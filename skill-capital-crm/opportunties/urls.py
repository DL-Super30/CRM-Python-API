# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OpportunityViewSet

router = DefaultRouter()
router.register(r'opportunties', OpportunityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
