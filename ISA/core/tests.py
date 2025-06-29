"""
Tests the essential functionality of:
- Customer model creation and validation
- Basic field constraints and defaults
"""

from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Customer


class CustomerModelTest(TestCase):
    """Essential tests for Customer model"""

    def test_customer_creation(self):
        """Test basic customer creation"""
        customer = Customer.objects.create(customer_name="Test Customer")

        self.assertEqual(customer.customer_name, "Test Customer")
        self.assertTrue(customer.active)
        self.assertIsNotNone(customer.date_created)
        self.assertIsNone(customer.customer_bio)

    def test_customer_with_bio(self):
        """Test customer creation with bio"""
        customer = Customer.objects.create(
            customer_name="Test Customer", customer_bio="Test bio", active=False
        )

        self.assertEqual(customer.customer_bio, "Test bio")
        self.assertFalse(customer.active)

    def test_customer_name_required(self):
        """Test that customer_name is required"""
        with self.assertRaises(IntegrityError):
            Customer.objects.create(customer_name=None)

    def test_customer_name_max_length(self):
        """Test customer_name max length validation"""
        long_name = "x" * 51

        with self.assertRaises(ValidationError):
            customer = Customer(customer_name=long_name)
            customer.full_clean()

    def test_date_created_auto_set(self):
        """Test that date_created is automatically set"""
        before = timezone.now()
        customer = Customer.objects.create(customer_name="Test Customer")
        after = timezone.now()

        self.assertGreaterEqual(customer.date_created, before)
        self.assertLessEqual(customer.date_created, after)

    def test_customer_auto_id(self):
        """Test that customer_id is auto-generated"""
        customer = Customer.objects.create(customer_name="Test Customer")
        self.assertIsNotNone(customer.customer_id)
        self.assertIsInstance(customer.customer_id, int)
