from django.db import models
from django.utils import timezone

# Create your models here.
class CreateLeads(models.Model):

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
        ('Not Contacted','Not Contacted'),
        ('Attempted','Attempted'),
        ('Warm Lead','Warm Lead'),
        ('Cold Lead','Cold Lead'),
    ]

    LEAD_SOURCE_CHOICES = [
        ('None', 'None'),
        ('WalkIn', 'WalkIn'),
        ('StudentReferral', 'StudentReferral'),
        ('Demo', 'Demo'),
        ('WebSite', 'WebSite'),
        ('WebsiteChat', 'WebsiteChat'),
        ('InboundCall', 'InboundCall'), 
        ('GoogleAdWords', 'GoogleAdWords'),
        ('FacebookAds', 'FacebookAds'),
        ('GoogleMyBusiness', 'GoogleMyBusiness'),
        ('WhatsAppSkillCapital', 'WhatsAppSkillCapital'),
        
    ]
    COURSES_CHOICES = [
        ('HR Business Partner','HR Business Partner'),
        ('HR Generalist Core HR','HR Generalist Core HR'),
        ('HR Analytics','HR Analytics'),
        ('Spoken English','Spoken English'),
        ('Public Speaking','Public Speaking'),
        ('Communication Skills','Communication Skills'),
        ('Soft Skills','Soft Skills'),
        ('Personality Development','Personality Development'),
        ('Aptitude','Aptitude'),
        ('IELTS','IELTS'),
        ('TOEFL','TOEFL'),
        ('PTE','PTE'),
        ('GRE','GRE'),
        ('GMAT','GMAT'),
        ('Recruitment Specialist','Recruitment Specialist'),
        ('Payroll Specialist','Payroll Specialist'),
        ('Learning and Development','Learning and Development'),
        ('Others','Others'),
        ('Finance','Finance'),
        ('Competitive Exams','Competitive Exams'),
        ('HR Manage','HR Manage'),
    ]
    
    CLASS_MODE_CHOICES = [
        ('International Online','International Online'),
        ('India Online','India Online'),
        ('BLR Classroom','BLR Classroom'),
        ('HYD Classroom','Hyd Classroom'),
    ]

    STACK_CHOICES = [
        ('Life Skills','Life Skills'),
        ('Study Abroad','Study Abroad'),
        ('HR','HR'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    cc = models.BigIntegerField()
    phone = models.BigIntegerField()
    email = models.EmailField(max_length=255)
    fee_quoted = models.DecimalField(max_digits=10, decimal_places=2)
    batch_timing = models.CharField(
        max_length=10,  # Adjusted max_length to fit the longest value
        choices=BATCH_TIMING_CHOICES,
        default='7AM_8AM',
    )
    
    description = models.TextField()
    Stack= models.CharField(
        max_length=24,
        choices=STACK_CHOICES,
        default='Select Stack',
    )
    Course = models.CharField(
        max_length=24,
        choices=COURSES_CHOICES,
        default='None',
    )
    lead_status = models.CharField(
        max_length=13,
        choices=LEAD_STATUS_CHOICES,
        default='None',
    )
    lead_source = models.CharField(
        max_length=24,
        choices=LEAD_SOURCE_CHOICES,
        default='None',
    )
    class_mode = models.CharField(
        max_length=24,
        choices=CLASS_MODE_CHOICES,
        default='HYDClassRoom',
    )
    next_fallow_up = models.DateField(default=timezone.now)
   
    
    
    
    

 

 