from django.urls import include, path
from rest_framework import routers
from accounts import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('plans/', views.PlanViewSet.as_view()),
    path('register/', views.RegisterUserAPIView.as_view()),
    path('login/', views.LoginUserAPIView.as_view()),
]
