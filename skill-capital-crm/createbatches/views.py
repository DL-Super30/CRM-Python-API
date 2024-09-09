from rest_framework import viewsets
from .models import CreateBatches, Batch
from .serializers import CreateBatchesSerializer, BatchSerializer

# CreateBatches ViewSet
class CreateBatchesViewSet(viewsets.ModelViewSet):
    queryset = CreateBatches.objects.all()
    serializer_class = CreateBatchesSerializer

# Batch ViewSet
class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer

