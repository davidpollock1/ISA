from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserProfile
from .serializers import UserProfileSerializer
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

@method_decorator(csrf_protect, name='dispatch')
class GetUserProfileView(APIView):
    def get(self, request, format=None):
        try:
            user = self.request.user
            username = user.username
        
            
            user_profile = UserProfile.objects.get(user=user)
            user_profile = UserProfileSerializer(user_profile)
            
            return Response({ 'profile': user_profile.data, 'username': str(username)})
        except:
            return Response({ 'error': 'Something went wrong retrieving the user profile'})
        
@method_decorator(csrf_protect, name='dispatch')   
class UpdateUserProfileView(APIView):
    def put(self, request, format=None):
        try:
            user = self.request.user
            username = user.username
            
            data = self.request.data
            
            fields_to_update = {}

            # Get all the fields in the UserProfile model
            model_fields = [field.name for field in UserProfile._meta.get_fields()]
            
            for field in model_fields:
                if field in data:
                    fields_to_update[field] = data[field]
            
            UserProfile.objects.filter(user=user).update(**fields_to_update)
            
            user_profile = UserProfile.objects.get(user=user)
            user_profile = UserProfileSerializer(user_profile)
            
            return Response({ 'profile': user_profile.data, 'username': str(username)})        
        except:
            return Response({ 'error': 'Something went wrong updating the user profile'})
