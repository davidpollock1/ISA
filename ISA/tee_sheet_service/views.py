from email.policy import HTTP
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from rest_framework import generics
from .models import TeeSheetSettings
from .serializers import TeeSheetSettingsSerializer
from ISA.permissions import IsCustomerData
from user_profile.models import UserProfile

# @method_decorator(csrf_protect, name='dispatch')
# class TeeSheetSettingsView(APIView):
#     permission_classes = ([CustomerAccessPermission])
#     def get(self, request, pk, format=None):
#         try:
                        
#             tee_sheet_settings = TeeSheetSettings.objects.get(tee_sheet_settings_id=pk)
            
#             return Response(tee_sheet_settings.data, status=status.HTTP_200_OK)
#         except:
#             return Response({ 'error': 'Something went wrong retrieving the user profile'})
        
#     def post(self, request, format=None):
#         try:
#             data = request.data
#             tee_sheet_settings = self.request.user.userprofile
            
#             if tee_sheet_settings.customer_id is None:
#                 return Response(status=status.HTTP_403_FORBIDDEN)
            
#             tee_sheet_settings_data = { **data, 'customer': tee_sheet_settings.customer.customer_id}
                
#             serializer = TeeSheetSettingsSerializer(data=tee_sheet_settings_data)
            
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as ex:
#             return Response(ex, status=status.HTTP_400_BAD_REQUEST)
        
@method_decorator(csrf_protect, name='dispatch')
class TeeSheetSettingsCreateView(generics.CreateAPIView):
    queryset = TeeSheetSettings.objects.all()
    serializer_class = TeeSheetSettingsSerializer
    permission_classes = [IsCustomerData]

    def perform_create(self, serializer):
        user_profile = UserProfile.objects.get(user=self.request.user)
        serializer.save(customer_id=user_profile.customer_id, created_by=self.request.user)