from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User



class UserDetails(models.Model):
    ROLES = (
        ('Designer', 'Designer'),
        ('User', 'User')
    )
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_details')
    role = models.CharField(max_length=100, choices=ROLES, default='User')
    contact_number = models.CharField(max_length=15)
    address = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)
    password = models.CharField(max_length=128)  
   

    def __str__(self) -> str:
        return self.user_id.username
    

class InteriorDesigner(models.Model):
    user_details = models.OneToOneField(UserDetails, on_delete=models.CASCADE, related_name='designer')
    years_of_experience = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    specializations = models.TextField(blank=True, null=True)
    portfolio = models.CharField(max_length=100)
    portfolio_link = models.URLField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.user_details.user_id.username
    
    
    
