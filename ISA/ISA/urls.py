from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("accounts/", include("accounts.urls")),
    path("golf_course/", include("golf_course_service.urls")),
    path("tee_sheets/", include("tee_sheet_service.urls")),
]

urlpatterns += [re_path(r"^.*", TemplateView.as_view(template_name="index.html"))]
