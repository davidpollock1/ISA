"""
Comprehensive test suite for the accounts app.

This module contains tests for:
- UserProfile model functionality and validation
- Serializers (Login, Signup, UserProfile)
- API views and endpoints
- Authentication and authorization
- Edge cases and error handling

Test Structure:
- UserProfileModelTest: Tests for the UserProfile model
- LoginSerializerTest: Tests for login serializer validation
- SignupSerializerTest: Tests for signup serializer and user creation
- UserProfileSerializerTest: Tests for profile serialization and updates
- AccountsAPITestCase: Integration tests for all API endpoints
- AccountsEdgeCasesTestCase: Edge cases and boundary conditions

Run with: python manage.py test accounts.tests
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .models import UserProfile
from .serializers import LoginSerializer, SignupSerializer, UserProfileSerializer
from core.models import Customer


class UserProfileModelTest(TestCase):
    """Test cases for UserProfile model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.customer = Customer.objects.create(
            customer_name="Test Customer", customer_bio="Test Bio"
        )

    def test_user_profile_creation(self):
        """Test UserProfile creation with default values"""
        profile = UserProfile.objects.create(user=self.user, email="test@example.com")
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.type, "public_user")
        self.assertEqual(profile.first_name, "")
        self.assertEqual(profile.last_name, "")
        self.assertEqual(profile.phone, "")
        self.assertEqual(profile.city, "")

    def test_user_profile_with_all_fields(self):
        """Test UserProfile creation with all fields"""
        profile = UserProfile.objects.create(
            user=self.user,
            type="tenant_admin",
            first_name="John",
            last_name="Doe",
            phone="1234567890",
            city="New York",
            email="john@example.com",
            customer=self.customer,
        )
        self.assertEqual(profile.first_name, "John")
        self.assertEqual(profile.last_name, "Doe")
        self.assertEqual(profile.type, "tenant_admin")
        self.assertEqual(profile.phone, "1234567890")
        self.assertEqual(profile.city, "New York")
        self.assertEqual(profile.customer, self.customer)

    def test_user_profile_str_method(self):
        """Test UserProfile __str__ method"""
        profile = UserProfile.objects.create(
            user=self.user, first_name="John", email="test@example.com"
        )
        self.assertEqual(str(profile), "John")

    def test_get_customer_method(self):
        """Test get_customer method"""
        profile = UserProfile.objects.create(
            user=self.user, email="test@example.com", customer=self.customer
        )
        self.assertEqual(profile.get_customer(), self.customer)

        profile_no_customer = UserProfile.objects.create(
            user=User.objects.create_user("test2", "test2@example.com", "pass"),
            email="test2@example.com",
        )
        self.assertIsNone(profile_no_customer.get_customer())

    def test_user_type_choices(self):
        """Test all user type choices are valid"""
        valid_types = [
            "tenant_admin",
            "tenant_user",
            "platform_admin",
            "support_staff",
            "public_user",
        ]
        for user_type in valid_types:
            profile = UserProfile.objects.create(
                user=User.objects.create_user(
                    f"user_{user_type}", f"{user_type}@example.com", "pass"
                ),
                type=user_type,
                email=f"{user_type}@example.com",
            )
            self.assertEqual(profile.type, user_type)


class LoginSerializerTest(TestCase):
    """Test cases for LoginSerializer"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_valid_login(self):
        """Test valid login credentials"""
        data = {"username": "testuser", "password": "testpass123"}
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        validated_data = serializer.validated_data
        self.assertEqual(validated_data["user"], self.user)

    def test_invalid_username(self):
        """Test login with invalid username"""
        data = {"username": "wronguser", "password": "testpass123"}
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("Invalid username or password", str(serializer.errors))

    def test_invalid_password(self):
        """Test login with invalid password"""
        data = {"username": "testuser", "password": "wrongpass"}
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("Invalid username or password", str(serializer.errors))

    def test_inactive_user(self):
        """Test login with inactive user"""
        self.user.is_active = False
        self.user.save()

        data = {"username": "testuser", "password": "testpass123"}
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        # Django's authenticate returns None for inactive users,
        # so it will show as invalid credentials
        self.assertIn("Invalid username or password", str(serializer.errors))


class SignupSerializerTest(TestCase):
    """Test cases for SignupSerializer"""

    def test_valid_signup(self):
        """Test valid signup data"""
        data = {
            "username": "newuser",
            "password": "newpass123",
            "re_password": "newpass123",
            "email": "new@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "1234567890",
            "city": "New York",
        }
        serializer = SignupSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_password_mismatch(self):
        """Test signup with password mismatch"""
        data = {
            "username": "newuser",
            "password": "newpass123",
            "re_password": "differentpass",
            "email": "new@example.com",
        }
        serializer = SignupSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("Passwords do not match", str(serializer.errors))

    def test_duplicate_username(self):
        """Test signup with existing username"""
        User.objects.create_user("existinguser", "existing@example.com", "pass")

        data = {
            "username": "existinguser",
            "password": "newpass123",
            "re_password": "newpass123",
            "email": "new@example.com",
        }
        serializer = SignupSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("Username already exists", str(serializer.errors))

    def test_user_creation(self):
        """Test actual user and profile creation"""
        data = {
            "username": "newuser",
            "password": "newpass123",
            "re_password": "newpass123",
            "email": "new@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "1234567890",
            "city": "New York",
        }
        serializer = SignupSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        user = serializer.save()
        self.assertEqual(user.username, "newuser")

        # Check that UserProfile was created
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(profile.first_name, "John")
        self.assertEqual(profile.last_name, "Doe")
        self.assertEqual(profile.phone, "1234567890")
        self.assertEqual(profile.city, "New York")
        self.assertEqual(profile.email, "new@example.com")

    def test_minimal_signup(self):
        """Test signup with minimal required fields"""
        data = {
            "username": "minuser",
            "password": "minpass123",
            "re_password": "minpass123",
            "email": "min@example.com",
        }
        serializer = SignupSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        user = serializer.save()
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(profile.first_name, "")
        self.assertEqual(profile.last_name, "")
        self.assertEqual(profile.phone, "")
        self.assertEqual(profile.city, "")


class UserProfileSerializerTest(TestCase):
    """Test cases for UserProfileSerializer"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.customer = Customer.objects.create(customer_name="Test Customer")
        self.profile = UserProfile.objects.create(
            user=self.user,
            first_name="John",
            last_name="Doe",
            phone="1234567890",
            city="New York",
            email="john@example.com",
            customer=self.customer,
        )

    def test_serialization(self):
        """Test profile serialization"""
        serializer = UserProfileSerializer(self.profile)
        data = serializer.data
        self.assertEqual(data["first_name"], "John")
        self.assertEqual(data["last_name"], "Doe")
        self.assertEqual(data["phone"], "1234567890")
        self.assertEqual(data["city"], "New York")
        self.assertEqual(data["email"], "john@example.com")

    def test_update(self):
        """Test profile update"""
        update_data = {"first_name": "Jane", "city": "Los Angeles"}
        serializer = UserProfileSerializer(self.profile, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())

        updated_profile = serializer.save()
        self.assertEqual(updated_profile.first_name, "Jane")
        self.assertEqual(updated_profile.city, "Los Angeles")
        self.assertEqual(updated_profile.last_name, "Doe")  # Should remain unchanged


class AccountsAPITestCase(APITestCase):
    """Test cases for Accounts API views"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            first_name="John",
            last_name="Doe",
            phone="1234567890",
            city="New York",
            email="test@example.com",
        )

    def test_signup_view(self):
        """Test user signup endpoint"""
        url = "/accounts/register"
        data = {
            "username": "newuser",
            "password": "newpass123",
            "re_password": "newpass123",
            "email": "new@example.com",
            "first_name": "Jane",
            "last_name": "Smith",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("success", response.data)
        self.assertIn("username", response.data)

        # Verify user was created
        self.assertTrue(User.objects.filter(username="newuser").exists())
        # Verify profile was created
        user = User.objects.get(username="newuser")
        self.assertTrue(UserProfile.objects.filter(user=user).exists())

    def test_signup_invalid_data(self):
        """Test signup with invalid data"""
        url = "/accounts/register"
        data = {
            "username": "newuser",
            "password": "pass",
            "re_password": "different",
            "email": "invalid-email",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_view(self):
        """Test user login endpoint"""
        url = "/accounts/login"
        data = {"username": "testuser", "password": "testpass123"}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("success", response.data)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        url = "/accounts/login"
        data = {"username": "testuser", "password": "wrongpass"}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_view(self):
        """Test user logout endpoint"""
        self.client.force_authenticate(user=self.user)
        url = "/accounts/logout"

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("success", response.data)

    def test_check_authenticated_view(self):
        """Test authentication check endpoint"""
        url = "/accounts/authenticated"

        # Test unauthenticated
        response = self.client.get(url)
        self.assertIn(
            response.status_code, [status.HTTP_200_OK, status.HTTP_403_FORBIDDEN]
        )
        if response.status_code == status.HTTP_200_OK:
            self.assertEqual(response.data["isAuthenticated"], "error")

        # Test authenticated
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["isAuthenticated"], "success")

    def test_get_csrf_token_view(self):
        """Test CSRF token endpoint"""
        url = "/accounts/csrf_cookie"

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("success", response.data)

    def test_delete_account_view(self):
        """Test account deletion endpoint"""
        self.client.force_authenticate(user=self.user)
        url = "/accounts/delete"

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIn("success", response.data)

        # Verify user was deleted
        self.assertFalse(User.objects.filter(username="testuser").exists())

    def test_delete_account_unauthenticated(self):
        """Test account deletion without authentication"""
        url = "/accounts/delete"

        response = self.client.delete(url)
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN],
        )

    def test_get_user_profile_view(self):
        """Test get user profile endpoint"""
        self.client.force_authenticate(user=self.user)
        url = "/accounts/profile/user"

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("user_profile", response.data)
        self.assertEqual(response.data["user_profile"]["first_name"], "John")

    def test_get_user_profile_unauthenticated(self):
        """Test get user profile without authentication"""
        url = "/accounts/profile/user"

        response = self.client.get(url)
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN],
        )

    def test_update_user_profile_view(self):
        """Test update user profile endpoint"""
        self.client.force_authenticate(user=self.user)
        url = "/accounts/profile/update"
        data = {"first_name": "Jane", "city": "Los Angeles"}

        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("user_profile", response.data)
        self.assertEqual(response.data["user_profile"]["first_name"], "Jane")
        self.assertEqual(response.data["user_profile"]["city"], "Los Angeles")

        # Verify changes in database
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.first_name, "Jane")
        self.assertEqual(self.profile.city, "Los Angeles")

    def test_update_user_profile_unauthenticated(self):
        """Test update user profile without authentication"""
        url = "/accounts/profile/update"
        data = {"first_name": "Jane"}

        response = self.client.patch(url, data, format="json")
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN],
        )


class AccountsEdgeCasesTestCase(APITestCase):
    """Additional edge case tests for accounts app"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.profile = UserProfile.objects.create(
            user=self.user, first_name="John", last_name="Doe", email="test@example.com"
        )

    def test_signup_with_whitespace_username(self):
        """Test signup with username containing whitespace"""
        url = "/accounts/register"
        data = {
            "username": "  spaced user  ",
            "password": "newpass123",
            "re_password": "newpass123",
            "email": "spaced@example.com",
        }

        response = self.client.post(url, data, format="json")
        # Should still work as Django handles username normalization
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_with_empty_fields(self):
        """Test login with empty username or password"""
        url = "/accounts/login"

        # Empty username
        data = {"username": "", "password": "testpass123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Empty password
        data = {"username": "testuser", "password": ""}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_profile_with_invalid_data(self):
        """Test updating profile with invalid data"""
        self.client.force_authenticate(user=self.user)
        url = "/accounts/profile/update"

        # Test with extremely long strings
        data = {
            "first_name": "x" * 300,
            "phone": "1" * 30,
        }

        response = self.client.patch(url, data, format="json")
        # Should fail validation
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_profile_user_without_profile(self):
        """Test getting profile for user without UserProfile"""
        # Create user without profile
        user_no_profile = User.objects.create_user(
            username="noprofile", password="testpass123"
        )

        self.client.force_authenticate(user=user_no_profile)
        url = "/accounts/profile/user"

        with self.assertRaises(Exception):
            self.client.get(url)

    def test_signup_with_very_long_password(self):
        """Test signup with extremely long password"""
        url = "/accounts/register"
        data = {
            "username": "longpassuser",
            "password": "x" * 1000,
            "re_password": "x" * 1000,
            "email": "longpass@example.com",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_multiple_login_attempts(self):
        """Test multiple login attempts with same credentials"""
        url = "/accounts/login"
        data = {"username": "testuser", "password": "testpass123"}

        # Multiple successful logins should work
        for _ in range(3):
            response = self.client.post(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_case_sensitive_username_login(self):
        """Test login with different case username"""
        url = "/accounts/login"

        # Try login with different case
        data = {
            "username": "TESTUSER",
            "password": "testpass123",
        }

        response = self.client.post(url, data, format="json")
        # Should fail as usernames are case-sensitive in Django
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_profile_update_partial_fields(self):
        """Test updating only specific profile fields"""
        self.client.force_authenticate(user=self.user)
        url = "/accounts/profile/update"

        original_last_name = self.profile.last_name

        # Update only first name
        data = {"first_name": "UpdatedName"}
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user_profile"]["first_name"], "UpdatedName")
        # Other fields should remain unchanged
        self.assertEqual(response.data["user_profile"]["last_name"], original_last_name)

    def test_user_type_validation(self):
        """Test UserProfile with invalid user type"""
        user = User.objects.create_user("testtype", "testtype@example.com", "pass")

        profile = UserProfile.objects.create(
            user=user,
            type="invalid_type",  # Not in choices
            email="testtype@example.com",
        )

        self.assertEqual(profile.type, "invalid_type")
