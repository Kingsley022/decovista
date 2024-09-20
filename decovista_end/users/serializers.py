from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
# from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from .models import UserDetails, DesignerDetails, User
from django.contrib.auth import authenticate


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['contact_number', 'address', 'profile_picture', 'created_at', 'updated_at']

class DesignerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignerDetails
        fields = ['years_of_experience', 'specializations', 'profile_picture', 'portfolio', 'portfolio_link', 'bio']

class CustomUserCreateSerializer(serializers.ModelSerializer):
    user_details = UserDetailsSerializer(required=False)
    designer_details = DesignerDetailsSerializer(required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'password', 'user_details', 'designer_details']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user_details_data = validated_data.pop('user_details', None)
        designer_details_data = validated_data.pop('designer_details', None)
        password = validated_data.pop('password')
        
        # Create the user
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        
        # Create UserDetails if provided
        if user_details_data:
            UserDetails.objects.create(user_id=user, **user_details_data)
        
        # Create DesignerDetails if provided and role is 'designer'
        if designer_details_data and user.role == 'designer':
            DesignerDetails.objects.create(user_details=user, **designer_details_data)
        
        return user

    def update(self, instance, validated_data):
        user_details_data = validated_data.pop('user_details', None)
        designer_details_data = validated_data.pop('designer_details', None)
        
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.role = validated_data.get('role', instance.role)
        
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        
        instance.save()
        
        if user_details_data:
            user_details = instance.user_details
            user_details.contact_number = user_details_data.get('contact_number', user_details.contact_number)
            user_details.address = user_details_data.get('address', user_details.address)
            user_details.profile_picture = user_details_data.get('profile_picture', user_details.profile_picture)
            user_details.save()

        if designer_details_data and instance.role == 'designer':
            designer_details = instance.designer_details
            designer_details.years_of_experience = designer_details_data.get('years_of_experience', designer_details.years_of_experience)
            designer_details.specializations = designer_details_data.get('specializations', designer_details.specializations)
            designer_details.profile_picture = designer_details_data.get('profile_picture', designer_details.profile_picture)
            designer_details.portfolio = designer_details_data.get('portfolio', designer_details.portfolio)
            designer_details.portfolio_link = designer_details_data.get('portfolio_link', designer_details.portfolio_link)
            designer_details.bio = designer_details_data.get('bio', designer_details.bio)
            designer_details.save()

        return instance


class CustomUserSerializer(serializers.ModelSerializer):
    user_details = UserDetailsSerializer(read_only=True)
    designer_details = DesignerDetailsSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'user_details', 'designer_details']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer to allow users to obtain JWT tokens using their email or username.
    """
    username = serializers.CharField(label="Username or Email")

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Authenticate using the custom backend
            user = authenticate(request=self.context.get('request'), username=username, password=password)

            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
                refresh = self.get_token(user)

                data = {}
                data['refresh'] = str(refresh)
                data['access'] = str(refresh.access_token)
                data.update({
                    'id':user.id,
                    'first_name':user.first_name,
                    'last_name':user.last_name,
                    'username':user.username,
                    'email':user.email,
                    'is_active':user.is_active
                })

                return data
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")
