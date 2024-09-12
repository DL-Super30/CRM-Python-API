from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=100,)
    
    

def __str__(self):
        return self.name

class Stack(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CreateBatches(models.Model):
    Location_CHOICES = {
        ('Hyderabad', 'Hyderabad'),
          
}

    name = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE,choices=Location_CHOICES, default='Hyderabd')  # Assuming a 'Location' model
    slot = models.CharField(max_length=100)
    trainer = models.CharField(max_length=100)
    timing = models.CharField(max_length=100)
    class_mode = models.CharField(max_length=100)
    stage = models.CharField(max_length=100)
    comment = models.CharField(max_length=100)
    learners = models.CharField(max_length=100)
    stack = models.ForeignKey(Stack, on_delete=models.CASCADE)  # Assuming a 'Stack' model
    start_date = models.DateField()
    end_date = models.DateField()
    batch_status = models.CharField(max_length=50)
    topic_status = models.CharField(max_length=50)
    no_of_students = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name
#month1,month2,month3
class Batch(models.Model):
    date = models.DateField()
    topic = models.CharField(max_length=200)
    start_time = models.TimeField()
    end_time = models.TimeField()
    attendance = models.IntegerField(default=0)  # Store attendance count
    video_upload = models.BooleanField(default=False)
    duration = models.DurationField()

    def __str__(self):
        return f"{self.topic} on {self.date}"
