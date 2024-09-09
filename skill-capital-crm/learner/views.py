# views.py

from rest_framework import viewsets
from .models import Learner
from .serializers import LearnerSerializer
from rest_framework import response # type: ignore
from rest_framework.status import HTTP_204_NO_CONTENT # type: ignore
# from rest_framework import permissions

class LearnerViewSet(viewsets.ModelViewSet):
    queryset = Learner.objects.all()
    serializer_class = LearnerSerializer
    # permission_classes = [permissions.IsAuthenticated]

def destroy(self, request, pk=None):
        
        instance = self.get_object()
        instance.delete()

        return response.Response({'messsage':"Record delete successfully"},status=HTTP_204_NO_CONTENT)



