from django.urls import path
from support.v1 import views

urlpatterns = [
    path('departmans/', views.DepartmansViewSet.as_view()),
]
