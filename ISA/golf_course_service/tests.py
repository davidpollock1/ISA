from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

class SuperUserCreateCustomerTest(TestCase):
    
    def setUp(self):
        self.staff_user = User.objects.create_user(username='staff_user', password='staff_user_password', is_staff=True)
        self.client.login(username='staff_user', password='staff_user_password')
        self.data = {'customer_name': 'customer_staff', 'active': 'True'}

    def test_can_create_user(self):
        response = self.client.post(reverse('customer'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
class UserCreateCustomerTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='user_password')
        self.client.login(username='user', password='user_password')
        self.data = {'customer_name': 'customer_user', 'active': 'True'}

    def test_can_create_user(self):
        response = self.client.post(reverse('customer'), self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)