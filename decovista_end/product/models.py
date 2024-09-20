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
    image_2 = models.ImageField(upload_to="product_designs/", null=True, blank=True)
    image_3 = models.ImageField(upload_to="product_designs/", null=True, blank=True)
    
    def __str__(self):
        return self.product_name


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.category_name
    

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    product = models.ForeignKey('Products', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_reviews")
    designer = models.ForeignKey('users.DesignerDetails', on_delete=models.CASCADE, related_name="designer_reviews")
    rating = models.IntegerField(default=1)  
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.review_id} for {self.product.product_name}"


