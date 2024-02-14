from django.db import models
from django.conf import settings
import datetime

        
class Events(models.Model):
    EVENT_TYPES = (
    (1, 'Lesson'),
    (2, 'Unavailable'),
    )
    events_id = models.BigAutoField(primary_key=True)
    requested_by_user_id = models.CharField(max_length=30, null=False)
    requested_for_user_id = models.CharField(max_length=30, null=False)
    event_date_time = models.DateTimeField(null=False)
    event_type = models.PositiveSmallIntegerField(choices=EVENT_TYPES, default=1)
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    date_last_updated = models.DateTimeField(auto_now=True, null=False)
    active = models.BooleanField(null=False, default=True)
    
    
    class Meta:
        verbose_name = "Events"
        ordering = ('date_created'),
    
    def __str__(self) -> str:
        return self.requested_by_user_id, self.requested_for_user_id, self.event_date_time
    
    
class LessonRequest(models.Model):
    REQUEST_STATUSES = (
    (1, 'Requested'),
    (2, 'Accepted'),
    (3, 'Denied'),
    )
    lesson_request_id = models.BigAutoField(primary_key=True)
    instructor_id = models.ForeignKey('user_profile.Instructor', on_delete=models.CASCADE)
    student_id = models.ForeignKey('user_profile.Student', on_delete=models.CASCADE)
    
    requested_datetime = models.DateTimeField(null=False)
    date_created = models.DateTimeField(null=False, auto_now_add=True)
    
    lesson_duration = models.DurationField(null=False)
    lesson_type = models.CharField(max_length=30)
    lesson_address = models.CharField(max_length=255, blank=True, null=True)
    
    status = models.PositiveSmallIntegerField(choices=REQUEST_STATUSES, default=1)
    notes = models.CharField(max_length=250, blank=True, null=True)

class EventStudent(models.Model):
    event_student_id = models.BigAutoField(primary_key=True)
    event_id = models.ForeignKey(Events, on_delete=models.CASCADE)
    student_id = models.ForeignKey('user_profile.Student', on_delete=models.CASCADE)

class EventInstructor(models.Model):
    event_instructor_id = models.BigAutoField(primary_key=True)
    event_id = models.ForeignKey(Events, on_delete=models.CASCADE)
    instructor_id = models.ForeignKey('user_profile.Instructor', on_delete=models.CASCADE)