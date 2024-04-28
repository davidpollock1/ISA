from django.urls import path
from .views import CustomerView

urlpatterns = [
    path('customer', CustomerView.as_view()),
]
