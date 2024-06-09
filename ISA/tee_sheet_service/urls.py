from django.urls import path
from .views import TeeSheetSettingsView

urlpatterns = [
    path('tee_sheet', TeeSheetSettingsView.as_view(), name='tee-sheet'),
]