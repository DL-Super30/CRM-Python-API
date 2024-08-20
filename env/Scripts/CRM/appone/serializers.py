from rest_framework import serializers # type: ignore
from .models import CreateNewLead

class CreateNewLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateNewLead
        fields = '__all__'