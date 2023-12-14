from django.urls import path
from .views import EventCreationView, EventApprovedView, EventAllView, LessonRequestView

app_name='eventcalendar'

urlpatterns = [
    path('event/create', EventCreationView.as_view(), name='createevent'),
    path('event/approve', EventApprovedView.as_view(), name='approveevent'),
    path('event/all', EventAllView.as_view(), name='allevent'),
    path('event/request_lesson', LessonRequestView.as_view(), name='requestlesson')
] 
