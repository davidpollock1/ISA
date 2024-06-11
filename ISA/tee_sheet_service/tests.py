import json
from django.test import TestCase
from django.contrib.auth.models import User
from golf_course_service.models import GolfCourse, Customer
from user_profile.models import UserProfile
from .models import TeeSheetSettings
from django.urls import reverse
from rest_framework import status

class SuperUserCreateTeeSheetSetingsTest(TestCase):
    
    def setUp(self):
        self.staff_user = User.objects.create_user(username='staff_user', password='staff_user_password', is_staff=True)
        self.customer = Customer.objects.create(customer_id=7)
        self.golf_course = GolfCourse.objects.create(id=8, customer=self.customer)
        self.client.login(username='staff_user', password='staff_user_password')
        self.data = {
            'interval': '0 0:11:00',
            'start_time': '8:30:00',
            'end_time': '14:30:00',
            'number_of_slots': '4',
            'default_price': '15.25',
            'alternative_price': '10',
            'alternative_price_timespan': '0 02:00:00',
            'golf_course': '8',
            }

    def test_can_create_tee_sheet_settings(self):
        response = self.client.post(reverse('tee-sheet'), self.data)
        customer = TeeSheetSettings.objects.get(number_of_slots=self.data['number_of_slots'])
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(customer)
        