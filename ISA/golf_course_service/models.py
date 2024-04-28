from django.db import models
# from django.conf import settings
# import datetime


class Customer(models.Model):
    customer_id = models.BigAutoField(primary_key=True)
    customer_name = models.CharField(max_length=50, blank=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    date_last_updated = models.DateTimeField(auto_now=True, null=False)
    active = models.BooleanField(null=False, default=True)

class GolfCourse(models.Model):
    golf_course_name = models.CharField(max_length=50, blank=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    date_last_updated = models.DateTimeField(auto_now=True, null=False)
    active = models.BooleanField(null=False, default=True)
    
    customer_id = models.ForeignKey('Customer', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "GolfCourse"
        # ordering = ('date_created'),
    
    def __str__(self) -> str:
        return self.golf_course_id, self.golf_course_name, self.customer_id
        
class GolfCourseGroup(models.Model):
    golf_courses = models.ManyToManyField(GolfCourse)
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    date_last_updated = models.DateTimeField(auto_now=True, null=False)
    active = models.BooleanField(null=False, default=True)
    
    customer_id = models.ForeignKey('Customer', on_delete=models.CASCADE)
