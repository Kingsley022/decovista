from django.urls import path
from .views import UserDetailsListCreateAPIView, CustomUserCreateAPIView


urlpatterns = [
    path('user-details/', UserDetailsListCreateAPIView.as_view(), name='user-details-list-create'),
    path('', CustomUserCreateAPIView.as_view(), name='custom-user-create')
]
