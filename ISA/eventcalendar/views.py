import datetime
from rest_framework import status
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from.serializers import EventsSerializer, LessonRequestSerializer
from .models import Events, LessonRequest
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator

@method_decorator(csrf_protect, name = 'dispatch')
class EventCreationView(APIView):
    def post(self, request, format=None, event_data=None):
        if event_data is None:
            event_data = request.data

        serializer = EventsSerializer(data=event_data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def perform_create(self, serializer):
        serializer.save()
        
@method_decorator(csrf_protect, name = 'dispatch')    
class EventAllView(APIView):
    serializer = EventsSerializer
    
    def get(self, request):
        curr_user = self.request.user
        try:
            events = Events.objects.get(requested_for_user_id=curr_user.id)
            serializer = EventsSerializer(events, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Events.DoesNotExist:
            return Response({'error': 'No events found'}, status=status.HTTP_404_NOT_FOUND)

@method_decorator(csrf_protect, name = 'dispatch')    
class EventInRangeView(APIView):
    serializer = EventsSerializer
    
    def get(self, request, format=None):
        curr_user = self.request.user
        start_date_str = self.request.data.get('start_date', '')
        end_date_str = self.request.data.get('end_date', '')

        try:
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            events = Events.objects.filter(requested_for_user_id=curr_user.id,
                                           event_date_time__range=[start_date, end_date])
            
            serializer = EventsSerializer(events, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Events.DoesNotExist:
            return Response({'error': 'No events found'}, status=status.HTTP_404_NOT_FOUND)

@method_decorator(csrf_protect, name = 'dispatch')    
class LessonRequestView(APIView):
    def post(self, request, format=None):
        try:
            data = request.data
            user_profile = self.request.user.userprofile
            student_record = user_profile.student

            lesson_request_data = {'student_id': student_record.student_id, **data}
            
            serializer = LessonRequestSerializer(data=lesson_request_data)
            
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Something went wrong creating the instructor record. {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def perform_create(self, serializer):
        serializer.save()
        
@method_decorator(csrf_protect, name = 'dispatch')    
class LessonApprovedView(APIView):
    lesson_request_serializer = LessonRequestSerializer
    
    def patch(self, request, format=None):
        lesson_request_id = request.data.get('lesson_request_id')
        if not lesson_request_id:
            return Response({'error': 'lesson_request_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            lesson_request = LessonRequest.objects.get(lesson_request_id=lesson_request_id)
        except LessonRequest.DoesNotExist:
            return Response({'error': 'Lesson request not found'}, status=-status.HTTP_404_NOT_FOUND)
        
        serializer = self.lesson_request_serializer(lesson_request, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            
            serializer.save(status=2)
            
            # To do - Clean up Event & Lesson Request models. Currently only allows requests and approval one way. Student -> Instructor.
            event_data = {
                'requested_by_user_id_id': lesson_request.student_id.student_id,
                'requested_for_user_id': lesson_request.instructor_id.instructor_id,
                'event_date_time': lesson_request.requested_datetime,
                'event_type' : 1,
                'active' : True,
            }
            event_view = EventCreationView()
            event_response = event_view.post(request=None, event_data=event_data)

            return Response({
                'lesson_request': serializer.data,
                'event': event_response.data
            })

        return Response(serializer.data)
