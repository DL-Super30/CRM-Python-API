from django.db import models
from django.utils import timezone

class Learner(models.Model):
    BATCH_TIMING_CHOICES = [
        ('7AM_8AM', '7AM_8AM'),
        ('8AM_9AM', '8AM_9AM'),
        ('9AM_10AM', '9AM_10AM'),
        ('10AM_11AM', '10AM_11AM'),
        ('11AM_12PM', '11AM_12PM'),
        ('12PM_1PM', '12PM_1PM'),
        ('1PM_2PM', '1PM_2PM'),
        ('2PM_3PM', '2PM_3PM'),
        ('3PM_4PM', '3PM_4PM'),
        ('4PM_5PM', '4PM_5PM'),
        ('5PM_6PM', '5PM_6PM'),
        ('6PM_7PM', '6PM_7PM'),
        ('7PM_8PM', '7PM_8PM'),
        ('8PM_9PM', '8PM_9PM'),
    ]
    LEAD_STATUS_CHOICES = [
        ('None', 'None'),
        ('NotContacted', 'NotContacted'),
        ('Attempted', 'Attempted'),
        ('WarmLead', 'WarmLead'),
        ('Opportunity', 'Opportunity'),
        ('AttendedDemo', 'AttendedDemo'),
        ('Visited', 'Visited'),
        ('Registered', 'Registered'),
        ('ColdLead', 'ColdLead'),
    ]

    TECH_STACK_CHOICES = [
        ('CloudOps', 'CloudOps'),
        ('Salesforce', 'Salesforce'),
        ('FullStack', 'FullStack'),
        ('DataStack', 'DataStack'),
        ('ServiceNow', 'ServiceNow'),
        ('BusinessStack', 'BusinessStack'),
        ('CareerCounselling', 'CareerCounselling'),
    ]

    CLASS_MODE_CHOICES = [
        ('HYDClassRoom', 'HYDClassRoom'),
        ('BLRClassRoom', 'BLRClassRoom'),
        ('IndiaOnline', 'IndiaOnline'),
        ('InternationalOnline', 'InternationalOnline'),
    ]
    name = models.CharField(max_length=255)
    cc = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    fee_quoted = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    batch_timing = models.CharField(max_length=100, blank=True, null=True,  # Adjusted max_length to fit the longest value
        choices=BATCH_TIMING_CHOICES,
        default='7AM_8AM',)
    lead_status = models.CharField(max_length=50,
        choices=LEAD_STATUS_CHOICES,
        default='None',)
    opportunity_status = models.CharField(max_length=50)
    opportunity_stage = models.CharField(max_length=50)
    demo_attended_stage = models.CharField(max_length=50)
    visited_stage = models.CharField(max_length=50)
    cold_lead_reason = models.CharField(max_length=255)
    next_followup = models.DateField(blank=True, null=True)
    lead_source = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
