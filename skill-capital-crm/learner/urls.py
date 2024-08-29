# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LearnerViewSet

router = DefaultRouter()
router.register(r'learner', LearnerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
