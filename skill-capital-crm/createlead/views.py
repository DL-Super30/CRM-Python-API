from django.shortcuts import render
from rest_framework import viewsets


from .models import CreateLeads
from .serializers import CreateLeadsSerializer
# Create your views here.

class CreateLeadsViewSet(viewsets.ModelViewSet):

    queryset = CreateLeads.objects.all()
    serializer_class = CreateLeadsSerializer
