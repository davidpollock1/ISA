from rest_framework import serializers
from .models import Events, LessonRequest

class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields =['requested_by_user_id', 'requested_for_user_id', 'event_date_time', 'event_type', 'active', 'approved']
    
    requested_by_user_id = serializers.ReadOnlyField(source='requested_by_user_id.user')
    
class LessonRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonRequest
        fields = '__all__'