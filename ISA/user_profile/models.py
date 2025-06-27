from django.db import models
from django.contrib.auth.models import User
from core.models import TenantAwareModel

class UserProfile(TenantAwareModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    phone = models.CharField(max_length=20, default='')
    city = models.CharField(max_length=25, default='')
    email = models.EmailField()
    
    def __str__(self):
        return self.first_name
    
    def get_customer(self):
        if(self.customer):
            return self.customer
        
        return None
    
    class Meta:
        verbose_name = "UserProfile"
        db_table = 'USER_PROFILE'