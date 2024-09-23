# # urls.py

# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import LearnerViewSet

# router = DefaultRouter()
# router.register(r'learner', LearnerViewSet)
# # router.register(r'CourseDeatails', LearnerViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LocationViewSet, LearnerViewSet, CourseDetailsViewSet

router = DefaultRouter()
router.register(r'locations', LocationViewSet)
router.register(r'learners', LearnerViewSet,basename='learner')
router.register(r'coursedetails', CourseDetailsViewSet,basename='CourseDetails')

urlpatterns = [
    path('', include(router.urls)),
]
