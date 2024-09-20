from django.urls import path
from .views import UserDetailsListCreateAPIView, CustomUserCreateAPIView, CurrentUserAPIView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('user-details/', UserDetailsListCreateAPIView.as_view(), name='user-details-list-create'),
    path('get-create-user/', CustomUserCreateAPIView.as_view(), name='custom-user-create'),
    path('user/', CurrentUserAPIView.as_view(), name='current_user'),
    
    # Custom JWT Token endpoints
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
