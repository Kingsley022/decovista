from django.db import models
from users.models import User

# Create your models here.

class Consultation(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    consultation_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    designer = models.ForeignKey('InteriorDesigner', on_delete=models.CASCADE)
    scheduled_datetime = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Consultation {self.consultation_id} with {self.designer.user_details.user.username}"


class Designer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    

    def __str__(self):
        return self.name

