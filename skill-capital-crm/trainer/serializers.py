from rest_framework import serializers
from .models import Trainer

class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = ['name', 'description', 'id_proof', 'trainer_status', 'batches', 
                  'batch_stage', 'free_slots', 'tech_stack', 'phone', 'email', 'location']
