from django.urls import path
from .views import CustomerView, GolfCourseView, GolfCourseGroupView

urlpatterns = [
    path('customer', CustomerView.as_view(), name='customer'),
    path('golf_course', GolfCourseView.as_view(), name='golf-course'),
    path('golf_course_group', GolfCourseGroupView.as_view(), name='golf-course-group'),
]
