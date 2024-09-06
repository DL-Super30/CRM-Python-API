from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreateBatchesViewSet, BatchViewSet

router = DefaultRouter()
router.register(r'createbatches', CreateBatchesViewSet)
router.register(r'batches', BatchViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
