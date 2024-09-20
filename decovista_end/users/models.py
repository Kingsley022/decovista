from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
# Create your models here.


# class User(AbstractUser):
#     email = models.EmailField(unique=True)

#     def __str__(self) -> str:
#         return self.username


class UserDetails(models.Model):
    ROLES = (
        ('designer', 'Designer'),
        ('user', 'User')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_details')
    role = models.CharField(max_length=100, choices=ROLES, default='user')
    contact_number = models.CharField(max_length=15)
    address = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self) -> str:
        return self.user_id.username
    

class InteriorDesigner(models.Model):
    user_details = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='designer')
    years_of_experience = models.IntegerField()
    specialization = models.CharField(max_length=100)
    portfolio = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user_details.user_id.username
    
    
    
