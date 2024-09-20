from django.db import models

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_image = models.ImageField(upload_to='products/')
    product_quantity = models.PositiveIntegerField()
    product_amount  = models.DecimalField()

    def __str__(self):
        return self.product_name

