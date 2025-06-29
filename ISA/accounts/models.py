from django.db import models
from django.contrib.auth.models import User
from core.models import TenantOptionalModel


class UserProfile(TenantOptionalModel):
    USER_TYPES = (
        ("tenant_admin", "Tenant Administrator"),
        ("tenant_user", "Tenant User"),
        # global user types
        ("platform_admin", "Platform Administrator"),
        ("support_staff", "Support Staff"),
        ("public_user", "Public User"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=USER_TYPES, default="public_user")
    first_name = models.CharField(max_length=255, default="")
    last_name = models.CharField(max_length=255, default="")
    phone = models.CharField(max_length=20, default="")
    city = models.CharField(max_length=25, default="")
    email = models.EmailField()

    def __str__(self):
        return self.first_name

    def get_customer(self):
        if self.customer:
            return self.customer

        return None

    class Meta:
        verbose_name = "UserProfile"
        db_table = "USER_PROFILE"
