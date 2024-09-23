from django.db import models
from django.utils import timezone

class Opportunity(models.Model):
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
    
    STACK_CHOICES = [
        ('Life Skills', 'Life Skills'),
        ('Study Abroad', 'Study Abroad'),
        ('HR', 'HR'),
    ]
    
    CLASS_MODE_CHOICES = [
        ('International Online', 'International Online'),
        ('India Online', 'India Online'),
        ('BLR Classroom', 'BLR Classroom'),
        ('HYD Classroom', 'Hyd Classroom'),
    ]
    
    opportunity_status_choices = [
        ('Visiting', 'Visiting'),
        ('visited', 'visited'),
        ('Demo Attended', 'Demo Attended'),
        ('Lost Opportunity', 'Lost Opportunity'),
    ]
    
    opportunity_stage_choices = [
        ('Select Opportunity Stage', 'Select Opportunity Stage'),
        ('None', 'None'),
        ('advanced_discussion', 'Advanced Discussion'),
        ('ready_to_join', 'Ready To Join'),
        ('visiting', 'Visiting'),
        ('fees_negotiation', 'Fees Negotiation'),
        ('batch_allocation', 'Batch Allocation'),
        ('interested_in_demo', 'Interested in Demo'),
        ('need_time_this_week', 'Need Time This Week'),
        ('need_time_next_week', 'Need Time Next Week'),
        ('need_time_this_month', 'Need Time This Month'),
        ('needs_time_next_month', 'Needs Time Next Month'),
        ('special_requirements', 'Special Requirements'),
        ('payment_link_sent', 'Payment Link Sent'),
        ('closed_won_registered', 'Closed Won Registered'),
        ('Busy & Asked a call back', 'Busy & Asked a call back'),
        ('Closed Lost', 'Closed Lost'),
    ]
    
    DEMO_ATTENDED_STAGE_CHOICES = [
        ('none', 'None'),
        ('ready_to_join', 'Ready to Join'),
        ('advanced_discussion', 'Advanced Discussion'),
        ('call_not_answered', 'Call Not Answered'),
        ('visiting', 'Visiting'),
        ('fees_negotiation', 'Fees Negotiation'),
        ('batch_allocation', 'Batch Allocation'),
        ('need_time_this_week', 'Need Time This Week'),
        ('need_time_next_week', 'Need Time Next Week'),
        ('need_time_this_month', 'Need Time This Month'),
        ('needs_time_next_month', 'Needs Time Next Month'),
        ('special_requirements', 'Special Requirements'),
        ('closed_won_registered', 'Closed Won (Registered)'),
        ('closed_lost_cold_lead', 'Closed Lost (Cold Lead)'),
    ]
    
    VISITED_STAGE_CHOICES = [
        ('none', 'None'),
        ('call_not_answered', 'Call Not Answered'),
        ('ready_to_join', 'Ready To Join'),
        ('fees_negotiation', 'Fees Negotiation'),
        ('batch_allocation', 'Batch Allocation'),
        ('interested_demo', 'Interested Demo'),
        ('special_requirements', 'Special Requirements'),
        ('need_time_this_week', 'Need Time This Week'),
        ('need_time_next_week', 'Need Time Next Week'),
        ('need_time_this_month', 'Need Time This Month'),
        ('need_time_next_month', 'Need Time Next Month'),
        ('closed_won_registered', 'Closed Won(Registered)'),
        ('closed_lost_cold_lead', 'Closed Lost(Cold Lead)'),
    ]
    
    LOST_OPPORTUNITY_REASON_CHOICES = [
        ('none', 'None'),
        ('invalid_number', 'Invalid Number'),
        ('not_interested', 'Not Interested'),
        ('joined_another_institute', 'Joined another institute'),
        ('asking_free_course', 'Asking free course'),
        ('pay_after_placement', 'Pay after Placement'),
    ]

    # Fields
    name = models.CharField(max_length=255)
    cc = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    fee_quoted = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    batch_timing = models.CharField(
        max_length=100,  # Adjusted max_length to fit the longest value
        choices=BATCH_TIMING_CHOICES,
        default='7AM_8AM',
    )
    lead_status = models.CharField(
        max_length=50,
        choices=LEAD_STATUS_CHOICES,
        default='None',
    )
    Stack = models.CharField(
        max_length=24,
        choices=STACK_CHOICES,
        default='Select Stack',
    )
    class_mode = models.CharField(
        max_length=24,
        choices=CLASS_MODE_CHOICES,
        default='HYDClassRoom',
    )
    description = models.TextField(max_length=100,default='none',)
    opportunity_status = models.CharField(
        max_length=50,
        choices=opportunity_status_choices,
    )
    opportunity_stage = models.CharField(
        max_length=50,
        choices=opportunity_stage_choices,
    )
    demo_attended_stage = models.CharField(
        max_length=50,
        choices=DEMO_ATTENDED_STAGE_CHOICES,
        default='none',
    )
    visited_stage = models.CharField(
        max_length=50,
        choices=VISITED_STAGE_CHOICES,
        default='none',
    )
    lost_opportunity_reason = models.CharField(
        max_length=50,
        choices=LOST_OPPORTUNITY_REASON_CHOICES,
        default='none',
    )
    cold_lead_reason = models.CharField(max_length=255)
    next_followup = models.DateField(blank=True, null=True)
    lead_source = models.CharField(max_length=100)

    def __str__(self):
        return self.name
