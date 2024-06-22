from typing import Required
from rest_framework import serializers
from .models import TeeSheetSettings, TeeSheetTime, TeeTimeSlot
from golf_course_service.serializers import GolfCourseSerializer

class TeeSheetSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeeSheetSettings
        fields = '__all__'

class TeeTimeSlotSerializer(serializers.ModelSerializer):
    
    golf_course = GolfCourseSerializer(read_only=True)
    
    class Meta:
        model = TeeTimeSlot
        fields = '__all__'

class TeeSheetTimeSerializer(serializers.ModelSerializer):
    
    slots = TeeTimeSlotSerializer(many=True, read_only=True)
    
    class Meta:
        model = TeeSheetTime
        fields = '__all__'
        
class TeeSheetTimeGeneratorRequest(serializers.Serializer):
    tee_sheet_settings_id = serializers.IntegerField();
    start_date = serializers.DateField();
    end_date = serializers.DateField();

class TeeTimesFilterSerializer(serializers.Serializer):
    date = serializers.DateField(required=True)
    golf_course_group = serializers.IntegerField(required=False)
    golf_course = serializers.IntegerField(required=False)
    
    def validate(self, data):
        if not data.get('golf_course_group') and not data.get('golf_course'):
            raise serializers.ValidationError("Must provide golf_course or golf_course_group")
        return data