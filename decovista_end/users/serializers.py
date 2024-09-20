from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from .models import UserDetails, DesignerDetails, User

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['role', 'contact_number', 'address']

class DesignerDetailsSerializer(serializers.ModelSerializer):
    user_details = UserDetailsSerializer(required=False, many=True)

    class Meta:
        model = DesignerDetails
        fields = ['years_of_experience', 'specialization', 'portfolio', 'user_details']

class CustomUserCreateSerializer(BaseUserCreateSerializer):
    user_details = UserDetailsSerializer(required=False, many=True)
    designer = DesignerDetailsSerializer(required=False, many=True)

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = (
            'id', 'first_name', 'last_name',
            'username', 'email', 'password',
            'user_details', 'designer'
            )

    def create(self, validated_data):
        print(validated_data, 'valid')
        user_details_data = validated_data.pop('user_details', None)
        designer_data = validated_data.pop('designer', None)
        user = super().create(validated_data)

        if user_details_data:
            for detail in  user_details_data:
                user_details = UserDetails.objects.create(user_id=user, **detail)

                if designer_data:
                    for data in designer_data:
                        InteriorDesigner.objects.create(user_details=user_details, **data)

        return user

    
    def validate(self, attrs):
        print("Validating data:", attrs)
        return super().validate(attrs)

class CustomUserSerializer(BaseUserSerializer):
    # user_details = UserDetailsSerializer(read_only=True, source='user_details.first') # Use .first() to get the first UserDetails object
    user_details = UserDetailsSerializer(read_only=True, many=True) # Use many=True to get multiple related objects,
    designer = DesignerDetailsSerializer(read_only=True, source='user_details.designer')

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ('user_details', 'designer')
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        
        response['first_name'] = instance.first_name
        response['last_name'] = instance.last_name
        
        # Handle multiple user details
        user_details = instance.user_details.all()
        if user_details.exists():
            response['user_details'] = UserDetailsSerializer(user_details, many=True).data
        else:
            response['user_details'] = []

        # Handle designer (assuming one-to-one or one-to-many relationship)
        try:
            designer = user_details.first().designer if user_details.exists() else None
            if designer:
                response['designer'] = DesignerDetailsSerializer(designer).data
            else:
                response['designer'] = None
        except AttributeError:
            response['designer'] = None

        return response

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