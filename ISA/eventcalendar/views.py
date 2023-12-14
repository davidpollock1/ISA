from rest_framework import status
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from.serializers import EventsSerializer, LessonRequestSerializer
from .models import Events
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator


class EventCreationView(APIView):
    def post(self, request):
        serializer = EventsSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_create(self, serializer):
        serializer.save(requested_by_user_id=self.request.user)
        

class EventApprovedView(APIView):
    serializer = EventsSerializer
    
    def patch(self, request, format=None):
        event_id = request.data.get('event_id')
        if not event_id:
            return Response({'error': 'event_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            event = Events.objects.get(id=event_id)
        except Events.DoesNotExist:
            return Response({'error': 'Event not found'}, status=-status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer(event, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(approved=True)  # Update the 'approved' field to True

        return Response(serializer.data)
    
class EventAllView(APIView):
    serializer = EventsSerializer
    
    def get(self, request):
        curr_user = self.request.user
        try:
            events = Events.objects.get(requested_for_user_id=curr_user.id)
            return Response(events, status=status.HTTP_201_CREATED)
        except Events.DoesNotExist:
            return Response({'error': 'No events found'}, status=-status.HTTP_404_NOT_FOUND)


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
