from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, UserDetailsSerializer, InteriorDesignerSerializer
from .models import UserDetails, InteriorDesigner, User


# Create your views here.


class UserDetailsListCreateAPIView(APIView):
    def get(self, request):
        user_details = UserDetails.objects.all()
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


class InteriorDesignerListCreateAPIView(APIView):
    def get(self, request, format=None):
        designers = InteriorDesigner.objects.all()
        serializer = InteriorDesignerSerializer(designers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = InteriorDesignerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InteriorDesignerDetailsAPIView(APIView):
    def get_object(self, pk):
        try:
            return InteriorDesigner.objects.get(pk=pk)
        except InteriorDesigner.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        designer = self.get_object(pk)
        serializer = InteriorDesignerSerializer(designer)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        designer = self.get_object(pk)
        serializer = InteriorDesignerSerializer(designer, data=request.data)
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