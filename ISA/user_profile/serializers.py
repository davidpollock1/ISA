from rest_framework import serializers
from .models import UserProfile, Student, Instructor

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        
class StudentSerializer(serializers.ModelSerializer):
    class Meta:       
        model = Student
        fields = '__all__'

class InstructorSerializer(serializers.ModelSerializer):
    class Meta:       
        model = Instructor
        fields = '__all__'