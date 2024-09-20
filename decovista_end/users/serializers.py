from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from .models import UserDetails, InteriorDesigner

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['role', 'contact_number', 'address']

class InteriorDesignerSerializer(serializers.ModelSerializer):
    user_details = UserDetailsSerializer()

    class Meta:
        model = InteriorDesigner
        fields = ['years_of_experience', 'specialization', 'portfolio', 'user_details']

class CustomUserCreateSerializer(BaseUserCreateSerializer):
    user_details = UserDetailsSerializer(required=False)
    designer = InteriorDesignerSerializer(required=False)

    class Meta(BaseUserCreateSerializer.Meta):
        fields = BaseUserCreateSerializer.Meta.fields + ('user_details', 'designer')

    def create(self, validated_data):
        user_details_data = validated_data.pop('user_details', None)
        designer_data = validated_data.pop('designer', None)
        user = super().create(validated_data)

        if user_details_data:
            user_details = UserDetails.objects.create(user_id=user, **user_details_data)

            if designer_data:
                InteriorDesigner.objects.create(user_details=user_details, **designer_data)

        return user

class CustomUserSerializer(BaseUserSerializer):
    # user_details = UserDetailsSerializer(read_only=True, source='user_details.first') # Use .first() to get the first UserDetails object
    user_details = UserDetailsSerializer(read_only=True, many=True) # Use many=True to get multiple related objects,
    designer = InteriorDesignerSerializer(read_only=True, source='user_details.designer')

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ('user_details', 'designer')


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