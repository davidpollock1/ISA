from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserProfile
from .serializers import UserProfileSerializer, StudentSerializer, InstructorSerializer
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
        
@method_decorator(csrf_protect, name='dispatch')
class StudentCreationView(APIView):
    def post(self, request, format=None):
        try:
            data = request.data
            user_profile = self.request.user.userprofile  # Assuming you have a userprofile attribute in the user model

            # Combine user_profile data with request data
            student_data = {'user_profile': user_profile.id, **data}
            
            serializer = StudentSerializer(data=student_data)
            
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Something went wrong creating the student record. {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def perform_create(self, serializer):
        serializer.save()

@method_decorator(csrf_protect, name='dispatch')
class InstructorCreationView(APIView):
    def post(self, request, format=None):
        try:
            data = request.data
            user_profile = self.request.user.userprofile  # Assuming you have a userprofile attribute in the user model

            # Combine user_profile data with request data
            instructor_data = {'user_profile': user_profile.id, **data}
            
            serializer = InstructorSerializer(data=instructor_data)
            
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Something went wrong creating the instructor record. {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def perform_create(self, serializer):
        serializer.save()
