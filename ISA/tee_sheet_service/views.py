from tracemalloc import start
from xmlrpc.client import ResponseError
from rest_framework import status
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import TeeSheetSettings, TeeSheetTime, TeeTimeSlot
from .serializers import TeeSheetSettingsSerializer, TeeSheetTimeGeneratorRequest, TeeTimesFilterSerializer, TeeSheetTimeSerializer
from ISA.permissions import IsCustomerData
from .utils import generate_tee_times, generate_tee_time_slots

@method_decorator(csrf_protect, name='dispatch')
class TeeSheetSettingsCreateView(APIView):
        
    permission_classes = ([IsCustomerData])
    
    def post(self, request, *args, **kwargs):
            serializer = TeeSheetSettingsSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                try:
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except Exception as ex:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@method_decorator(csrf_protect, name='dispatch')
class TeeSheetTimeGeneratorView(APIView):
    
    permission_classes = ([IsCustomerData])

    def post(self, request, format=None):
        serializer = TeeSheetTimeGeneratorRequest(data=request.data)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            tee_sheet_settings_id = validated_data['tee_sheet_settings_id']
            start_date = validated_data['start_date']
            end_date = validated_data['end_date']
            try:
                tee_sheet_settings = TeeSheetSettings.objects.get(tee_sheet_settings_id = tee_sheet_settings_id)
                            
                tee_sheet_times = generate_tee_times(tee_sheet_settings=tee_sheet_settings, start_date=start_date, end_date=end_date)
                
                TeeSheetTime.objects.bulk_create(tee_sheet_times)
                
                for tee_sheet_time in tee_sheet_times:
                    tee_sheet_time.save()
                    tee_time_slots = generate_tee_time_slots(tee_sheet_time, tee_sheet_settings.number_of_slots)
                    TeeTimeSlot.objects.bulk_create(tee_time_slots)
                
            except Exception as ex: 
                return Response(ex, status=status.HTTP_400_BAD_REQUEST)
            
@method_decorator(csrf_protect, name='dispatch')
class TeeSheetView(APIView):
    
    permission_classes = ([])

    def get(self, request, format=None):
        serializer = TeeTimesFilterSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            date = validated_data['date']
            golf_course_group = validated_data.get('golf_course_group')
            golf_course = validated_data.get('golf_course')
            
            try:
                queryset = TeeSheetTime.objects.filter(time__date=date)
                if golf_course_group:
                    queryset = queryset.filter(golf_course_group=golf_course_group)
                if golf_course:
                    queryset = queryset.filter(golf_course=golf_course)

                results = TeeSheetTimeSerializer(queryset, many=True).data
                return Response(results, status=status.HTTP_200_OK)
            except Exception as ex:
                Response(ex, status=status.HTTP_400_BAD_REQUEST)