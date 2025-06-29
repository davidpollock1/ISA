from django.urls import path
from .views import (
    SignupView,
    GetCSRFToken,
    LoginVIew,
    LogoutView,
    CheckAuthenticatedView,
    DeleteAccountView,
    GetUserProfileView,
    UpdateUserProfileView,
)

urlpatterns = [
    path("authenticated", CheckAuthenticatedView.as_view()),
    path("login", LoginVIew.as_view()),
    path("logout", LogoutView.as_view()),
    path("csrf_cookie", GetCSRFToken.as_view()),
    path("register", SignupView.as_view()),
    path("delete", DeleteAccountView.as_view()),
    path("profile/user", GetUserProfileView.as_view()),
    path("profile/update", UpdateUserProfileView.as_view()),
]
