from tokenize import blank_re
from django.db import models

class tee_sheet_settings(models.Model):
    tee_sheet_settings_id = models.BigAutoField(primary_key=True)
    
    interval = models.DurationField(blank=False, null=False)
    start_time = models.TimeField(blank=False, null=False)
    end_time =models.TimeField(blank=False, null=False)
    number_of_slots = models.PositiveIntegerField(blank=False, null=False, default=4)
    default_price = models.DecimalField(max_digits=6, decimal_places=2)
    alternative_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    alternative_price_timespan = models.DurationField(blank=True,null=False)
        
    golf_course = models.ForeignKey('GolfCourse', on_delete=models.RESTRICT)
    customer = models.ForeignKey('Customer', on_delete=models.RESTRICT)
    
class tee_sheet_time(models.Model):
    tee_sheet_time_id = models.BigAutoField(primary_key=True)
    time = models.DateTimeField(blank=False, null=False)
    golf_course = models.ForeignKey('GolfCourse', on_delete=models.RESTRICT)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    tee_sheet_settings = models.ForeignKey('tee_sheet_settings', on_delete=models.RESTRICT)
    customer = models.ForeignKey('Customer', on_delete=models.RESTRICT)

class tee_time_slot(models.Model):
    STATUSES = ((1, 'Available'),(2, 'Booked'),(3, 'On_Hold'))
    tee_time_slot_id = models.BigAutoField(primary_key=True)
    status = models.PositiveSmallIntegerField(choices=STATUSES)
    
    tee_sheet_time = models.ForeignKey('tee_sheet_time', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.RESTRICT)
    user = models.ForeignKey('Userprofile', on_delete=models.RESTRICT)
    # probably need relationship to order here. Pending... 
