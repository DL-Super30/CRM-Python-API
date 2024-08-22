from django.db import models

class Lead(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    stack = models.CharField(max_length=100)
    course = models.CharField(max_length=100)

    def __str__(self):
        return self.name

