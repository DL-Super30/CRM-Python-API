from django.db import models
from django.utils import timezone

class Campaign(models.Model):
    STATUS_CHOICES = [
        ('select_campaign_name', 'select_campaign_name'),
        ('upcoming', 'upcoming'),
        ('ongoing', 'ongoing'),
        ('onhold', 'onhold'),
        ('completed', 'Completed'),
    ]

    campaign_name = models.CharField(max_length=255)
    campaign_type = models.CharField(max_length=255)
    campaign_status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    campaign_date = models.DateField()
    campaign_end_date = models.DateField()

    def __str__(self):
        return self.campaign_name
