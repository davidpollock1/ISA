from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Customer, GolfCourse, GolfCourseGroup
from .serializers import CustomerSerializer, GolfCourseSerializer, GolfCourseGroupSerializer
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator


@method_decorator(csrf_protect, name='dispatch')
class CustomerView(APIView):
    
    permission_classes = (permissions.IsAuthenticated, )
    
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
    
    def get(self, request, pk, format=None):
        try:
            customer = Customer.objects.get(customer_id=pk)
            serializer = CustomerSerializer(customer, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({'error': 'No customer found'}, status=status.HTTP_404_NOT_FOUND)
        
