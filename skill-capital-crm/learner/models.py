from django.db import models


# current_time = timezone.now()


# Use a list of tuples for choices (instead of a dictionary)
Location_CHOICES = [
    ('Hyderabad', 'Hyderabad'),
    ('Bangalore', 'Bangalore'),
]

class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Learner(models.Model):
    # Basic information
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    id_proof = models.CharField(max_length=255, blank=True, null=True)
    phone = models.IntegerField()
    date_of_birth = models.DateField(blank=True, null=True)
    email = models.EmailField(max_length=255)

    # Registration and location details
   
    registered_date = models.DateField(blank=True, default=None)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default='Hyderabad')
    batch_ids = models.CharField(max_length=255, blank=True, null=True)
    alternate_phone = models.CharField(max_length=15, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    attended_demo = models.CharField(max_length=255, blank=True, null=True)
   
    learner_owner = models.CharField(max_length=255, blank=True, null=True)
    learner_stage = models.CharField(max_length=255, blank=True, null=True)
    

    # Additional learner details
   
   
   
    currency = models.CharField(max_length=10, blank=True, null=True)
    
    lead_created_time = models.DateTimeField(blank=True, null=True)
    counseling_done_by = models.CharField(max_length=255, blank=True, null=True)
    
    
 
class CourseDetails(models.Model):
    # Course details
    registered_course = models.CharField(max_length=255)
    tech_stack = models.CharField(max_length=255)
    course_comments = models.TextField(blank=True, null=True)

    # Access information
    slack_access = models.BooleanField(default=False)
    lms_access = models.BooleanField(default=False)

    # Class and timing details
    preferable_time = models.DateTimeField(blank=True, null=True)
    batch_timing = models.DateTimeField(blank=True, null=True)
    mode_of_class = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    # def __str__(self):
    #     return f"{self.registered_course} - {self.learner_owner}"
