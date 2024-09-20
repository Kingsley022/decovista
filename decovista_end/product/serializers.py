from rest_framework.serializers import ModelSerializer
from .models import Products, Review, Category


class CategorySerializer(ModelSerializer):
    
    class Meta:
        model = Category
        fields = "__all__"


class ProductsSerializer(ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)
    class Meta:
        model = Products
        fields = "__all__"
        
class CategorySerializer(ModelSerializer):
    
    class Meta:
        model = Category
        fields = "__all__"


class ReviewSerializer(ModelSerializer):
    
    class Meta:
        model = Review
        fields = "__all__"