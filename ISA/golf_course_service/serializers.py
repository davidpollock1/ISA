from rest_framework import serializers
from .models import GolfCourse, GolfCourseGroup
from core.models import Customer

class GolfCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = GolfCourse
        fields = '__all__'
        
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class GolfCourseGroupSerializer(serializers.ModelSerializer):
    
    courses = GolfCourseSerializer(many=True, read_only=True)
    
    class Meta:
        model = GolfCourseGroup
        fields = '__all__'