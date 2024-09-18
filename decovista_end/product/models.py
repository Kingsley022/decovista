from django.db import models
from users.models import User

# Create your models here.

class Products(models.Model):
    designer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=100)
    category = models.ManyToManyField('Category', related_name="products")
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to="product_designs/")
    
    def __str__(self):
        return self.product_name


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.category_name
    
    