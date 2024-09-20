from django.db import models
<<<<<<< HEAD
from django.contrib.auth.models import User
=======
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User
>>>>>>> 9b04af2db3b7a24ac9658da3988d9f844dc6bf3c

class User(AbstractUser):
    ROLES = (
        ('designer', 'designer'),
        ('user', 'user')
    )
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=100, choices=ROLES, default='user')
    
    def __str__(self) -> str:
        return super().__str__()

class UserDetails(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_details')
    contact_number = models.CharField(max_length=15)
    address = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)  
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
   

    def __str__(self) -> str:
        return self.user_id.username
    

class DesignerDetails(models.Model):
<<<<<<< HEAD
    user_details = models.OneToOneField(UserDetails, on_delete=models.CASCADE, related_name='designer')
    years_of_experience = models.CharField(max_length=100)
    specializations= models.CharField(max_length=100)
=======
    user_details = models.OneToOneField(User, on_delete=models.CASCADE, related_name='designer_details')
    years_of_experience = models.CharField(max_length=100)
    specializations = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
>>>>>>> 9b04af2db3b7a24ac9658da3988d9f844dc6bf3c
    portfolio = models.CharField(max_length=100)
    portfolio_link = models.URLField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.user_details.username
    
    
    
