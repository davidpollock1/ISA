from django.urls import path
from .views import EventCreationView, LessonApprovedView, EventAllView, LessonRequestView, EventInRangeView

app_name='eventcalendar'

urlpatterns = [
    path('event/create', EventCreationView.as_view(), name='createevent'),
    path('event/approve', LessonApprovedView.as_view(), name='approvelesson'),
    path('event/all', EventAllView.as_view(), name='allevent'),
    path('event/request_lesson', LessonRequestView.as_view(), name='requestlesson'),
    path('event/all_in_range', EventInRangeView.as_view(), name='eventinrange')

] 
