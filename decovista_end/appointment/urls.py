from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from appointment import views

urlpatterns = [
    path('', views.ConsultationView.as_view()),
    path('<int:pk>/', views.ConsultationDetail.as_view()),
]

