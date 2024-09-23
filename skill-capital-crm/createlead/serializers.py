from rest_framework import serializers
from .models import CreateLeads

class CreateLeadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateLeads
        fields = '__all__'