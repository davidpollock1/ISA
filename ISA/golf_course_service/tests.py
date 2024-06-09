import json
from django.test import TestCase
from django.contrib.auth.models import User
from user_profile.models import UserProfile
from .models import Customer, GolfCourseGroup, GolfCourse
from django.urls import reverse
from rest_framework import status

class SuperUserCreateCustomerTest(TestCase):
    
    def setUp(self):
        self.staff_user = User.objects.create_user(username='staff_user', password='staff_user_password', is_staff=True)
        self.client.login(username='staff_user', password='staff_user_password')
        self.data = {'customer_name': 'customer_staff', 'active': 'True'}

    def test_can_create_user(self):
        response = self.client.post(reverse('customer'), self.data)
        customer = Customer.objects.get(customer_name=self.data['customer_name'])
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(customer)
        
class UserCreateCustomerTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='user_password')
        self.client.login(username='user', password='user_password')
        self.data = {
            'customer_name': 'customer_user', 
            'active': 'True'
            }

    def test_can_create_user(self):
        response = self.client.post(reverse('customer'), self.data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Customer.objects.exists())
        
class CustomerUserCreateGolfCourseGroup(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='user_password')
        self.customer = Customer.objects.create(customer_id=7)
        self.user_profile = UserProfile.objects.create(user=self.user, customer=self.customer)
        self.client.login(username='user', password='user_password')
        self.data = {
            'name':'Test Golf Course Group',
            'street_address':'123 Main St',
            'state':'CO',
            'zip_code':'80109',
            'active':'True'
        }
        
    def test_can_create_golf_course_group(self):
        response = self.client.post(reverse('golf-course-group'), data=json.dumps(self.data), content_type='application/json')
        golf_course_group = GolfCourseGroup.objects.get(name=self.data['name'])
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(golf_course_group)


class NonCustomerUserCreateGolfCourseGroup(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='user_password')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.client.login(username='user', password='user_password')
        self.data = {
            'name':'Test Golf Course Group',
            'street_address':'123 Main St',
            'state':'CO',
            'zip_code':'80109',
            'active':'True'
        }
        
    def test_can_create_golf_course_group(self):
        response = self.client.post(reverse('golf-course-group'), data=json.dumps(self.data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(GolfCourseGroup.objects.exists())

class CustomerUserCreateGolfCourse(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='user_password')
        self.customer = Customer.objects.create(customer_id=7)
        self.user_profile = UserProfile.objects.create(user=self.user, customer=self.customer)
        self.golf_course_group = GolfCourseGroup.objects.create(customer=self.customer)
        self.client.login(username='user', password='user_password')
        self.data = {
            'golf_course_name':'Foothills Strings',
            'golf_course_group':1,
            'active':'True'
        }
        
    def test_can_create_golf_course(self):
        response = self.client.post(reverse('golf-course'), data=json.dumps(self.data), content_type='application/json')
        golf_course = GolfCourse.objects.get(golf_course_name=self.data['golf_course_name'])
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(golf_course)

class NonCustomerUserCreateGolfCourse(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='user_password')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.client.login(username='user', password='user_password')
        self.data = {
            'golf_course_name':'Foothills Strings',
            'golf_course_group':1,
            'active':'True'
        }
        
    def test_can_create_golf_course(self):
        response = self.client.post(reverse('golf-course'), data=json.dumps(self.data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(GolfCourse.objects.exists())
