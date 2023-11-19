from django.urls import path
from .views import GetUserProfileView, UpdateUserProfileView, StudentCreationView, InstructorCreationView

urlpatterns = [
    path('user', GetUserProfileView.as_view()),
    path('update', UpdateUserProfileView.as_view()),
    path('create_student', StudentCreationView.as_view()),
    path('create_instructor', InstructorCreationView.as_view()),
]
