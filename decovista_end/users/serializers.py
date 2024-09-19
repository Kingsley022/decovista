from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer,  UserSerializer as BaseUserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import UserDetails, InteriorDesigner


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email']
        
        

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            'id', 'first_name',
            'last_name', 'email',
            'username', 'is_active',
        ]

    # def validate(self, attrs):
    #     validated_attrs = super().validate(attrs)
    #     username = validated_attrs.get('username')
        
    #     user = user.objects.get(username=username)
        
    #     if user.is_deactivated():
    #         raise ValidationError()
        
        
        
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user

        data.update({
            'id':user.id,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'username':user.username,
            'email':user.email,
            'is_active':user.is_active
        })

       

        return data

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = [
            'role', 'contact_number', 'address'
        ]