from rest_framework import serializers
from .models import Events, LessonRequest

class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields ='__all__'
    
    requested_by_user_id = serializers.ReadOnlyField(source='requested_by_user_id.user')
    
class LessonRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonRequest
        fields = '__all__'