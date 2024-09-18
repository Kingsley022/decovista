from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class UserDetails(models.Model):
    ROLES = (
        ('Designer', 'Designer'),
        ('User', 'User')
    )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_details')
    role = models.CharField(max_length=100, choices=ROLES, default='User')
    contact_number = models.CharField(max_length=15)
    
