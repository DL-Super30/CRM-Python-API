# # views.py

# from rest_framework import viewsets
# from .models import Learner
# from .serializers import LearnerSerializer
# from rest_framework import response # type: ignore
# from rest_framework.status import HTTP_204_NO_CONTENT # type: ignore
# # from rest_framework import permissions

# class LearnerViewSet(viewsets.ModelViewSet):
#     queryset = Learner.objects.all()
#     serializer_class = LearnerSerializer
#     # permission_classes = [permissions.IsAuthenticated]
    

# def destroy(self, request, pk=None):
        
#         instance = self.get_object()
#         instance.delete()

#         return response.Response({'messsage':"Record delete successfully"},status=HTTP_204_NO_CONTENT)

from rest_framework import viewsets
from .models import Location, Learner, CourseDetails
from .serializers import LocationSerializer, LearnerSerializer, CourseDetailsSerializer

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class LearnerViewSet(viewsets.ModelViewSet):
    queryset = Learner.objects.all()
    serializer_class = LearnerSerializer

class CourseDetailsViewSet(viewsets.ModelViewSet):
    queryset = CourseDetails.objects.all()
    serializer_class = CourseDetailsSerializer


