from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, UserDetailsSerializer, DesignerDetailsSerializer, CustomUserCreateSerializer
from .models import UserDetails, DesignerDetails, User


# Create your views here.

class CustomUserCreateAPIView(APIView):
    
    def get(self, request):
        users = User.objects.all()
        serializer = CustomUserCreateSerializer(users, many=True)
        return Response(serializer.data)
        
    
    def post(self, request):
        serializer = CustomUserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # This will invoke the create method in the serializer
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailsListCreateAPIView(APIView):
    def get(self, request):
        user_details = UserDetails.objects.all()
        print(user_details)
        serializer = UserDetailsSerializer(user_details, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = UserDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailsAPIViews(APIView):
    def get_object(self, pk):
        try:
            return UserDetails.objects.get(pk=pk)
        except UserDetails.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserDetailsSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserDetailsSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user_obj = self.get_object(pk)
        user_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DesignerDetailsListCreateAPIView(APIView):
    def get(self, request, format=None):
        designers = DesignerDetails.objects.all()
        serializer = DesignerDetailsSerializer(designers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DesignerDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DesignerDetailsDetailsAPIView(APIView):
    def get_object(self, pk):
        try:
            return DesignerDetails.objects.get(pk=pk)
        except DesignerDetails.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        designer = self.get_object(pk)
        serializer = DesignerDetailsSerializer(designer)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        designer = self.get_object(pk)
        serializer = DesignerDetailsSerializer(designer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        designer = self.get_object(pk)
        designer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=request.data.get('username'))
            if not user.is_active:
                return Response({'detail': 'Account not activated'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)

        return super().post(request, *args, **kwargs)