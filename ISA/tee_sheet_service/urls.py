from django.urls import path
from .views import TeeSheetSettingsCreateView

urlpatterns = [
    path('tee_sheet', TeeSheetSettingsCreateView.as_view(), name='tee-sheet'),
]