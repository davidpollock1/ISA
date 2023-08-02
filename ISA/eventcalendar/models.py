from django.db import models
from django.conf import settings
from users.models import MyUser
import datetime

        
class Events(models.Model):
    requested_by_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    requested_for_user_id = models.CharField(max_length=30, null=False)
    event_date_time = models.DateTimeField(null=False)
    event_type = models.CharField(max_length=30)
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    date_last_updated = models.DateTimeField(auto_now=True, null=False)
    active = models.BooleanField(null=False)
    approved = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Events"
        ordering = ('date_created'),
    
    def __str__(self) -> str:
        return self.requested_by_user_id, self.requested_for_user_id, self.event_date_time
