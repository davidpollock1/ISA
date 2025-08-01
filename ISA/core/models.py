from django.db import models


class Customer(models.Model):
    customer_id = models.BigAutoField(primary_key=True)
    customer_name = models.CharField(max_length=50, blank=False, null=False)
    customer_bio = models.CharField(max_length=50, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    active = models.BooleanField(null=False, default=True)

    class Meta:
        verbose_name = "Customer"
        db_table = "CUSTOMER"


class TenantAwareModel(models.Model):
    """For models that must belong to a tenant"""

    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, null=False, blank=False
    )

    class Meta:
        abstract = True


class TenantOptionalModel(models.Model):
    """For models that can optionally belong to a tenant"""

    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, null=True, blank=True
    )

    class Meta:
        abstract = True
