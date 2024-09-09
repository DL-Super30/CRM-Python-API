from rest_framework import generics
from .models import Trainer
from .serializers import TrainerSerializer

class TrainerCreateView(generics.CreateAPIView):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer
