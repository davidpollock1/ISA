from rest_framework import serializers
from .models import TeeSheetSettings, TeeSheetTime, TeeTimeSlot

class TeeSheetSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeeSheetSettings
        fields = '__all__'

class TeeSheetTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeeSheetTime
        fields = '__all__'

class TeeTimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeeTimeSlot
        fields = '__all__'
        
class TeeSheetTimeGeneratorRequest(serializers.Serializer):
    tee_sheet_settings_id = serializers.IntegerField();
    start_date = serializers.DateField();
    end_date = serializers.DateField();
