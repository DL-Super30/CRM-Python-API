
from django.db import models

class Course(models.Model):
    course_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    course_image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    course_fee = models.DecimalField(max_digits=10, decimal_places=2)
    course_brochure = models.FileField(upload_to='course_brochures/', blank=True, null=True)

    def __str__(self):
        return self.course_name
