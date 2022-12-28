from django.urls import include, path
from rest_framework import routers
from accounts.v1 import views

urlpatterns = [
    path('plans/', views.PlanViewSet.as_view()),
    path('register/', views.RegisterUserAPIView.as_view()),
    path('login/', views.LoginUserAPIView.as_view()),
]
