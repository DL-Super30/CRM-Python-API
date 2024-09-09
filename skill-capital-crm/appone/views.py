from django.shortcuts import render
from rest_framework import viewsets # type: ignore
from rest_framework import response # type: ignore
from rest_framework.status import HTTP_204_NO_CONTENT # type: ignore
# from rest_framework import permissions

from .models import CreateNewLead
from .serializers import CreateNewLeadSerializer

# Create your views here.

class CreateNewLeadViewSet(viewsets.ModelViewSet):

    queryset = CreateNewLead.objects.all()
    serializer_class = CreateNewLeadSerializer
    # permission_classes=[permissions.IsAuthenticated]

    def destroy(self, request, pk=None):
        
        instance = self.get_object()
        
        instance.delete()

        return response({'messsage':"Record delete successfully"},status=HTTP_204_NO_CONTENT)
