from django.db import models
from core.models import TenantAwareModel

        
class GolfCourse(TenantAwareModel):
    golf_course_name = models.CharField(max_length=50, blank=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    date_last_updated = models.DateTimeField(auto_now=True, null=False)
    active = models.BooleanField(null=False, default=True)
    
    golf_course_group = models.ForeignKey('GolfCourseGroup', on_delete=models.RESTRICT)
    
    class Meta:
        verbose_name = "GolfCourse"
        db_table = 'GOLF_COURSE'
        # ordering = ('date_created'),
    
    def __str__(self) -> str:
        return self.golf_course_id, self.golf_course_name, self.customer_id
        
class GolfCourseGroup(TenantAwareModel):
    name = models.CharField(max_length=50, blank=False, null=False)
    street_address = models.CharField(max_length=50, blank=False, null=False)
    state = models.CharField(max_length=3, blank=False, null=False)
    zip_code = models.CharField(max_length=5, blank=False, null=False)
    active = models.BooleanField(null=False, default=True)
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    date_last_updated = models.DateTimeField(auto_now=True, null=False)
        
    class Meta:
        verbose_name = "GolfCourseGroup"
        db_table = 'GOLF_COURSE_GROUP'
