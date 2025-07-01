from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import login, logout
from rest_framework.response import Response
from .models import UserProfile
from .serializers import (
    LoginSerializer,
    SignupSerializer,
    UserSerializer,
    UserProfileSerializer,
)
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator


@method_decorator(csrf_protect, name="dispatch")
class CheckAuthenticatedView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({"isAuthenticated": request.user.is_authenticated})


class CurrentUserView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        if not request.user.is_authenticated:
            return Response(
                {"isAuthenticated": False, "user": None, "profile": None},
                status=status.HTTP_200_OK,
            )

        user = request.user
        user_profile = UserProfile.objects.get(user=user)

        user_serializer = UserSerializer(user)
        profile_serializer = UserProfileSerializer(user_profile)

        return Response(
            {
                "isAuthenticated": True,
                "user": user_serializer.data,
                "profile": profile_serializer.data,
            },
            status=status.HTTP_200_OK,
        )


@method_decorator(csrf_protect, name="dispatch")
class SignupView(APIView):
    permission_classes = (AllowAny,)

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
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        login(request, user)

        return Response(
            {"success": True, "username": user.username, "email": user.email},
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    def post(self, request, format=None):
        logout(request)
        return Response(
            {"success": "Logged Out"},
            status=status.HTTP_200_OK,
        )


@method_decorator(ensure_csrf_cookie, name="dispatch")
class GetCSRFToken(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        return Response({"success": "CSRF cookie set"})


class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, format=None):
        user = request.user
        username = user.username
        user.delete()
        return Response(
            {"success": f"User '{username}' has been deleted."},
            status=status.HTTP_204_NO_CONTENT,
        )


@method_decorator(csrf_protect, name="dispatch")
class GetUserProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        user = request.user
        user_profile = UserProfile.objects.get(user=user)

        serializer = UserProfileSerializer(instance=user_profile)

        return Response(
            {"user_profile": serializer.data},
            status=status.HTTP_200_OK,
        )


@method_decorator(csrf_protect, name="dispatch")
class UpdateUserProfileView(APIView):
    def patch(self, request, format=None):
        user_profile = request.user.userprofile
        serializer = UserProfileSerializer(
            user_profile, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"user_profile": serializer.data},
            status=status.HTTP_200_OK,
        )
