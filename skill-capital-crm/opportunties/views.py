# views.py

from rest_framework import viewsets
from .models import Opportunity
from .serializers import OpportunitySerializer
from .models import Opportunity
from rest_framework import response # type: ignore
from rest_framework.status import HTTP_204_NO_CONTENT # type: ignore
from rest_framework import permissions

class OpportunityViewSet(viewsets.ModelViewSet):
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer
    permission_classes=[permissions.IsAuthenticated]
    
def destroy(self, request, pk=None):
        
        instance = self.get_object()
        instance.delete()

        return response.Response({'messsage':"Record delete successfully"},status=HTTP_204_NO_CONTENT)



