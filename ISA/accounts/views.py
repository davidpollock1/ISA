from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import permissions, status
from django.contrib import auth
from rest_framework.response import Response
from .models import UserProfile
from .serializers import SignupSerializer, UserSerializer, UserProfileSerializer
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator


@method_decorator(csrf_protect, name="dispatch")
class CheckAuthenticatedView(APIView):
    def get(self, request, format=None):
        user = self.request.user
        try:
            isAuthenticated = user.is_authenticated

            if isAuthenticated:
                return Response({"isAuthenticated": "success"})
            else:
                return Response({"isAuthenticated": "error"})
        except:
            Response(
                {"error": "Something went wrong when checking authentication status"}
            )


@method_decorator(csrf_protect, name="dispatch")
class SignupView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        return Response(
            {"success": "User created successfully", "username": user.username},
            status=status.HTTP_201_CREATED,
        )


@method_decorator(csrf_protect, name="dispatch")
class LoginVIew(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data = self.request.data

        username = data["username"]
        password = data["password"]
        try:
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return Response({"success": "User authenticated", "username": username})
            else:
                return Response({"error": "Error Authenticating"})
        except:
            return Response({"error": "Something went wrong when loggin in"})


class LogoutView(APIView):
    def post(self, request, format=None):
        try:
            auth.logout(request)
            return Response({"success": "Logged Out"})
        except:
            return Response({"error": "Something went wrong when logging out"})


@method_decorator(ensure_csrf_cookie, name="dispatch")
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        return Response({"success": "CSRF cookie set"})


class DeleteAccountView(APIView):
    def delete(self, request, format=None):
        user = self.request.user
        try:
            user = User.objects.filter(id=user.id).delete()

            return Response({"success": "User deleted successfully"})
        except:
            return Response(
                {"error": "Something went wrong when trying to delete user"}
            )


class GetUsersView(APIView):
    permission_classes = (permissions.AllowAny,)

    serializer = UserSerializer

    def get(self, request, format=None):
        users = User.objects.all()

        users = UserSerializer(users, many=True)
        return Response(users.data)


@method_decorator(csrf_protect, name="dispatch")
class GetUserProfileView(APIView):
    def get(self, request, format=None):
        try:
            user = self.request.user
            username = user.username

            user_profile = UserProfile.objects.get(user=user)
            user_profile = UserProfileSerializer(user_profile)

            return Response({"profile": user_profile.data, "username": str(username)})
        except:
            return Response(
                {"error": "Something went wrong retrieving the user profile"}
            )


@method_decorator(csrf_protect, name="dispatch")
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

            return Response({"profile": user_profile.data, "username": str(username)})
        except:
            return Response({"error": "Something went wrong updating the user profile"})
