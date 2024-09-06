from django.db import models

class CreateBatches(models.Model):
    name = models.CharField(max_length=100)
    location = models.ForeignKey()
    slot = models.CharField(max_length=100)
    trainer = models.CharField(max_length=100)
    timing = models.CharField(max_length=100)
    class_mode = models.CharField(max_length=100)
    stage = models.CharField(max_length=100)
    comment = models.CharField(max_length=100)
    learners = models.CharField(max_length=100)
    stack = models.ForeignKey(on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    batch_status = models.CharField(max_length=50)
    topic_status = models.CharField(max_length=50)
    no_of_students = models.IntegerField()
