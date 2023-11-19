from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    phone = models.CharField(max_length=20, default='')
    city = models.CharField(max_length=25, default='')
    email = models.EmailField()
    
    def __str__(self):
        return self.first_name
    
    
class Student(models.Model):
    # Override ID field. 
    student_id = models.BigAutoField(primary_key=True)
    
    # Link to UserProfile
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    student_bio = models.CharField(max_length=200, blank=True)

class Instructor(models.Model):
    REQUEST_STATUSES = (
    (1, 'NEW'),
    (2, 'ACTIVE'),
    (3, 'AWAY'),
    (4, 'DEACTIVATED'),
    )
    # Override ID field.
    instructor_id = models.BigAutoField(primary_key=True)
    
    # Link to UserProfile
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    status = models.PositiveSmallIntegerField(choices=REQUEST_STATUSES, default=1)
    instructor_bio = models.CharField(max_length=200, blank=True)
    
    
class InstructorStudent(models.Model):
    # Override ID field.
    instructor_student_id = models.BigAutoField(primary_key=True)
    
    # Link
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='instructor_students')
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    