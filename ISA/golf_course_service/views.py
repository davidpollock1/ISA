from rest_framework import status
from .permissions import CustomerAccessPermission, GolfCourseAccessPermission
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Customer, GolfCourse, GolfCourseGroup
from .serializers import CustomerSerializer, GolfCourseSerializer, GolfCourseGroupSerializer
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator


@method_decorator(csrf_protect, name='dispatch')
class CustomerView(APIView):
    
    permission_classes = ([CustomerAccessPermission])
    
    def post(self, request, format=None, customer_data=None):
        try:
            if customer_data is None:
                customer_data = request.data
                
            serializer = CustomerSerializer(data=customer_data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, pk, format=None):
        try:
            customer = Customer.objects.get(customer_id=pk)
            serializer = CustomerSerializer(customer, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({'error': 'No customer found'}, status=status.HTTP_404_NOT_FOUND)
        


@method_decorator(csrf_protect, name='dispatch')
class GolfCourseView(APIView):
    
    permission_classes = ([GolfCourseAccessPermission])
    
    def post(self, request, format=None):
        try:
            data = request.data
            user_profile = self.request.user.userprofile
            golf_course_group = GolfCourseGroup.objects.get(id=data['golf_course_group'])
            
            self.check_object_permissions(request, golf_course_group)
            
            if user_profile.customer_id is None:
                return Response(status=status.HTTP_403_FORBIDDEN)
            
            golf_course_data = { **data, 'customer': user_profile.customer.customer_id}
                
            serializer = GolfCourseSerializer(data=golf_course_data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                # Return validation errors
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response(ex, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, pk, format=None):
        try:
            golf_course = GolfCourse.objects.get(golf_course_id=pk)
            
            serializer = GolfCourseSerializer(golf_course, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({'error': 'No golf course found'}, status=status.HTTP_404_NOT_FOUND)
        
@method_decorator(csrf_protect, name='dispatch')
class GolfCourseGroupView(APIView):
    
    permission_classes = ([GolfCourseAccessPermission])
    
    def post(self, request, format=None):
        try:
            data = request.data
            user_profile = self.request.user.userprofile
            
            if user_profile.customer_id is None:
                return Response(status=status.HTTP_403_FORBIDDEN)
            
            golf_course_group_data = { **data, 'customer': user_profile.customer.customer_id}
                
            serializer = GolfCourseGroupSerializer(data=golf_course_group_data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response(ex, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, pk, format=None):
        try:
            golf_course = GolfCourse.objects.get(golf_course_id=pk)
            
            serializer = GolfCourseSerializer(golf_course, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({'error': 'No golf course found'}, status=status.HTTP_404_NOT_FOUND)