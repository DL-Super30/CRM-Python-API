from django.db import models

class Trainer(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    id_proof = models.FileField(upload_to='id_proofs/')
    trainer_status = models.CharField(max_length=50, choices=[('Active', 'Active'), ('Inactive', 'Inactive')])
    batches = models.CharField(max_length=100)  # You can modify this based on your actual logic
    batch_stage = models.CharField(max_length=100)
    free_slots = models.IntegerField(default=0)
    tech_stack = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    location = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

