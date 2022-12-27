from django.urls import include, path
from rest_framework import routers
from accounts import views


urlpatterns = [
    path('plans/', views.PlanViewSet.as_view()),
    path('register/', views.UserList.as_view()),
]
