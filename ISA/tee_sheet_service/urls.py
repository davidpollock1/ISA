from django.urls import path
from .views import TeeSheetSettingsCreateView, TeeSheetTimeGeneratorView

urlpatterns = [
    path('tee_sheet_settings/', TeeSheetSettingsCreateView.as_view(), name='tee-sheet'),
    path('tee_sheet_generator/', TeeSheetTimeGeneratorView.as_view(), name='tee-sheet-generator'),
]