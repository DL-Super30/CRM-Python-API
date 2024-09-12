from rest_framework import serializers
from .models import CreateBatches, Batch

class CreateBatchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateBatches
        fields = "__all__"

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = "__all__"
