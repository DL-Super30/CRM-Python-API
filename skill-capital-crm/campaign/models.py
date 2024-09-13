from django.db import models
from django.utils import timezone

class Campaign(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('completed', 'Completed'),
    ]

    campaign_name = models.CharField(max_length=255)
    campaign_type = models.CharField(max_length=255)
    campaign_status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    campaign_date = models.DateField()
    campaign_end_date = models.DateField()

    def __str__(self):
        return self.campaign_name
