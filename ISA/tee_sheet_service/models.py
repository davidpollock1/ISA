from django.db import models
from core.models import TenantAwareModel


class TeeSheetSettings(TenantAwareModel):
    tee_sheet_settings_id = models.BigAutoField(primary_key=True)

    interval = models.DurationField(blank=False, null=False)
    start_time = models.TimeField(blank=False, null=False)
    end_time = models.TimeField(blank=False, null=False)
    number_of_slots = models.PositiveIntegerField(blank=False, null=False, default=4)
    default_price = models.DecimalField(max_digits=6, decimal_places=2)
    alternative_price = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True
    )
    alternative_price_timespan = models.DurationField(blank=True, null=False)

    golf_course = models.ForeignKey(
        "golf_course_service.GolfCourse", on_delete=models.RESTRICT
    )

    class Meta:
        verbose_name = "TeeSheetSettings"
        db_table = "TEE_SHEET_SETTINGS"


class TeeSheetTime(TenantAwareModel):
    tee_sheet_time_id = models.BigAutoField(primary_key=True)
    time = models.DateTimeField(blank=False, null=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    tee_sheet_settings = models.ForeignKey(
        "TeeSheetSettings", on_delete=models.RESTRICT
    )
    golf_course = models.ForeignKey(
        "golf_course_service.GolfCourse", on_delete=models.RESTRICT
    )

    class Meta:
        verbose_name = "TeeSheetTime"
        db_table = "TEE_SHEET_TIME"


class TeeTimeSlot(TenantAwareModel):
    STATUSES = ((1, "Available"), (2, "Booked"), (3, "On_Hold"))
    tee_time_slot_id = models.BigAutoField(primary_key=True)
    status = models.PositiveSmallIntegerField(choices=STATUSES)

    tee_sheet_time = models.ForeignKey("TeeSheetTime", on_delete=models.CASCADE)
    user = models.ForeignKey(
        "accounts.Userprofile", on_delete=models.RESTRICT, null=True
    )
    # probably need relationship to order here. Pending...

    class Meta:
        verbose_name = "TeeTimeSlots"
        db_table = "TEE_TIME_SLOT"
