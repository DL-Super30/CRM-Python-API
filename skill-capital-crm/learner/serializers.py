# # serializers.py

# from rest_framework import serializers
# from .models import Learner,CourseDetails

# class LearnerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Learner
#         fields = '__all__'
# class CourseDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CourseDetails
#         fields = '__all__'
from rest_framework import serializers
from .models import Location, Learner, CourseDetails

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name']

class LearnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Learner
        fields = '__all__'

class CourseDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDetails
        fields = '__all__'

